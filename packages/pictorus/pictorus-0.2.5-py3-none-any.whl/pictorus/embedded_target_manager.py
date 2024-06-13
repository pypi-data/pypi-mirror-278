import re
import fnmatch
from concurrent import futures

from pyocd.core.session import Session
from pyocd.core.helpers import ConnectHelper
from pyocd.target.pack.pack_target import is_pack_target_available
from pyocd.probe.debug_probe import DebugProbe
from pyocd.flash.file_programmer import FileProgrammer
from pyocd.target import TARGET
import cmsis_pack_manager as cp

from .exceptions import CommandError
from .logging_utils import get_logger
from .target_manager import TargetManager, CommandCtxt
from .command import DeployTarget
from .constants import EMPTY_ERROR

logger = get_logger()


def _get_matches(cache: cp.Cache, target: str):
    pat = re.compile(fnmatch.translate(target).rsplit("\\Z")[0], re.IGNORECASE)
    return {name for name in cache.index.keys() if pat.search(name)}


def _get_target_name(probe: DebugProbe):
    board_info = probe.associated_board_info
    return board_info.target if board_info else None


def _is_target_installed(target_name: str):
    return (target_name in TARGET) or is_pack_target_available(target_name, Session.get_current())


def _install_target(target_name: str):
    logger.info(f"Installing OCD target: {target_name}")

    cache = cp.Cache(True, False)
    matches = _get_matches(cache, target_name)
    if not matches:
        logger.error(f"Could not find OCD target: {target_name}")
        return

    devices = [cache.index[dev] for dev in matches]
    packs = cache.packs_for_devices(devices)
    logger.info("Downloading packs:")
    for pack in packs:
        logger.info("    " + str(pack))

    cache.download_pack_list(packs)


def _determine_target_name():
    probe = ConnectHelper.choose_probe(
        blocking=False,
        return_first=True,
    )
    if not probe:
        return None

    return _get_target_name(probe)


class EmbeddedTargetManager(TargetManager):
    def _deploy_app(self, target: DeployTarget, cmd_ctxt: CommandCtxt):
        self._target_state.error_log = EMPTY_ERROR.copy()
        # This can return None if no targets are found. Need to check this
        # before attempting to use as a ContextManager
        target_name = target.options.get("ocd_target", _determine_target_name())
        if not target_name:
            logger.error("Unable to determine target type")
            msg = "Unable to choose target type. Verify target is connected and powered on."
            raise CommandError("TargetFlashError", msg)

        target_available = _is_target_installed(target_name)
        if not target_available:
            # Make sure the target index is installed
            futures.wait([cmd_ctxt.updates_mgr.ocd_update_future])
            _install_target(target_name)

        session = ConnectHelper.session_with_chosen_probe(
            blocking=False, return_first=True, target_override=target_name
        )

        if not session:
            logger.error("Failed to connect to target")
            raise CommandError(
                "TargetConnectionError",
                "Failed to connect to target. Make sure it is connected and powered on.",
            )

        # Connect to the target
        with session:
            # Create a file programmer and flash the ELF file
            try:
                FileProgrammer(session).program(self._bin_path, file_format="elf")
            except Exception as e:
                logger.error("Failed to flash target", exc_info=True)
                raise CommandError("TargetFlashError", f"Failed to flash target: {e}")

    def handle_set_ttl_cmd(self, cmd_ctxt: CommandCtxt):
        pass

    def handle_set_log_level_cmd(self, cmd_ctxt: CommandCtxt):
        pass

    def _control_app_running(self, run_app: bool):
        pass

    def open(self):
        pass

    def close(self):
        pass
