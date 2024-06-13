from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
import os

import requests


from .exceptions import CommandError
from .updates_manager import UpdatesManager
from .config import APP_ASSETS_DIR
from .target_state import TargetState
from .command import Command, DeployTarget, DeployTargetType, CmdType
from .logging_utils import get_logger
from .local_server import COMMS

logger = get_logger()


def _is_process_target(target: DeployTarget) -> bool:
    return target.type == DeployTargetType.PROCESS


def _download_file(file_path: str, url: str):
    """Download a file to specified path"""
    logger.info("Downloading url: %s to path: %s", url, file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with requests.get(url, stream=True) as req, open(file_path, "wb") as in_file:
        req.raise_for_status()
        for chunk in req.iter_content(chunk_size=8192):
            in_file.write(chunk)


class CommandCtxt:
    def __init__(self, cmd: Command, updates_mgr: UpdatesManager) -> None:
        self.cmd = cmd
        self.updates_mgr = updates_mgr

    def __eq__(self, __value: object) -> bool:
        # Convenience method for tests. We only care about the command data for now
        if not isinstance(__value, CommandCtxt):
            return False

        return self.cmd == __value.cmd


class TargetManager(ABC):
    def __init__(self, target: DeployTarget, target_state: TargetState) -> None:
        logger.info("Initializing %s target with ID: %s", target.type.value, target.id)
        self._target = target
        self._target_state = target_state
        self._assets_dir = os.path.join(APP_ASSETS_DIR, target.id)
        self._bin_path = os.path.join(self._assets_dir, "pictorus_managed_app")
        self._params_path = os.path.join(self._assets_dir, "diagram_params.json")

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    @property
    def target_state_data(self) -> dict:
        return self._target_state.to_dict()

    @property
    def target_data(self) -> dict:
        return self._target.to_dict()

    def handle_command(self, cmd_ctxt: CommandCtxt):
        """Handle a command"""
        cmd = cmd_ctxt.cmd
        try:
            if cmd.type == CmdType.UPDATE_APP:
                self.handle_update_app_cmd(cmd_ctxt)
            elif cmd.type == CmdType.SET_TELEMETRY_TLL:
                self.handle_set_ttl_cmd(cmd_ctxt)
            elif cmd.type == CmdType.SET_LOG_LEVEL:
                self.handle_set_log_level_cmd(cmd_ctxt)
            elif cmd.type == CmdType.RUN_APP:
                self.handle_run_app_cmd(cmd_ctxt)
            else:
                logger.warning("Unknown command: %s", cmd.type)
        except CommandError as e:
            logger.error("Failed to handle command: %s", e)
            self._target_state.error_log = {
                "err_type": e.err_type,
                "message": e.message,
            }
        except Exception as e:
            logger.error("Failed to handle command: %s", e, exc_info=True)
            self._target_state.error_log = {
                "err_type": "UnknownError",
                "message": f"Command failed: {e}",
            }

    def handle_update_app_cmd(self, cmd_ctxt: CommandCtxt):
        """Update the app version for this target"""
        self._download_app_files(cmd_ctxt.cmd)
        self._deploy_app(self._target, cmd_ctxt)

    @abstractmethod
    def handle_set_ttl_cmd(self, cmd_ctxt: CommandCtxt):
        """Set the telemetry ttl for this target"""
        pass

    @abstractmethod
    def handle_set_log_level_cmd(self, cmd_ctxt: CommandCtxt):
        """Set the log level for this target"""
        pass

    def handle_run_app_cmd(self, cmd_ctxt: CommandCtxt):
        """Control whether the app is running or not"""
        run_app = cmd_ctxt.cmd.data["run_app"]
        self._target_state.run_app = run_app
        self._control_app_running(run_app)

    @abstractmethod
    def _deploy_app(self, target: DeployTarget, cmd_ctxt: CommandCtxt):
        """Deploy the app to the target"""
        pass

    @abstractmethod
    def _control_app_running(self, run_app: bool):
        """Start/stop the app.

        This is used by some internal methods so is separated from
        the public method for handling commands
        """
        pass

    @abstractmethod
    def open(self):
        """Open the target manager"""
        pass

    @abstractmethod
    def close(self):
        """Close the target manager"""
        pass

    def _download_app_files(self, cmd: Command):
        build_hash = cmd.data.get("build_hash")
        app_bin_url = cmd.data.get("app_bin_url")
        params_hash = cmd.data.get("params_hash")
        params_url = cmd.data.get("params_url")

        params_valid = params_hash and params_url if _is_process_target(self._target) else True
        if not build_hash or not app_bin_url or not params_valid:
            logger.error("Invalid app update request: %s", cmd.data)
            raise CommandError("InvalidUpdateRequest", "Missing required fields for app update.")

        download_paths = []
        if self._target_state.build_hash != build_hash:
            logger.info("Updating binary")
            download_paths.append((self._bin_path, app_bin_url))

        if self._target_state.params_hash != params_hash and params_url:
            logger.info("Updating params")
            download_paths.append((self._params_path, params_url))

        if download_paths:
            self._control_app_running(False)
            with ThreadPoolExecutor(max_workers=len(download_paths)) as executor:
                futures = [
                    executor.submit(_download_file, path, url) for path, url in download_paths
                ]

            try:
                for fut in futures:
                    fut.result()
            except requests.exceptions.HTTPError:
                logger.error("Failed to update app", exc_info=True)
                raise CommandError("DownloadError", "Failed to download app files.")
            else:
                os.chmod(self._bin_path, 0o755)
                self._target_state.build_hash = build_hash
                self._target_state.params_hash = params_hash
                logger.info("Successfully updated app")
                # We need to clear telemetry whenever the app updates, so all signal lengths line up
                COMMS.clear()
        else:
            logger.info("Using cached app files")
