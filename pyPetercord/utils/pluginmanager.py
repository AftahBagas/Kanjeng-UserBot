import importlib
import sys
from pathlib import Path

from pyPetercord import CMD_HELP, LOAD_PLUG

from ..Config import Config
from ..core import LOADED_CMDS, PLG_INFO
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..core.session import petercord
from ..helpers.tools import media_type
from ..helpers.utils import (
    _format,
    _petercordtools,
    _petercordutils,
    install_pip,
    reply_id,
)
from .decorators import admin_cmd, sudo_cmd

LOGS = logging.getLogger("PetercordBot")


def load_module(shortname, plugin_path=None):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        path = Path(f"PyPetercord/plugins/{shortname}.py")
        name = "pyPetercord.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        LOGS.info("Successfully imported " + shortname)
    else:
        if plugin_path is None:
            path = Path(f"pyPetercord/plugins/{shortname}.py")
            name = f"pyPetercord.plugins.{shortname}"
        else:
            path = Path((f"{plugin_path}/{shortname}.py"))
            name = f"{plugin_path}/{shortname}".replace("/", ".")
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.bot = petercord
        mod.LOGS = LOGS
        mod.Config = Config
        mod._format = _format
        mod.tgbot = petercord.tgbot
        mod.sudo_cmd = sudo_cmd
        mod.CMD_HELP = CMD_HELP
        mod.reply_id = reply_id
        mod.admin_cmd = admin_cmd
        mod._petercordutils = _petercordutils
        mod._petercordtools = _petercordtools
        mod.media_type = media_type
        mod.edit_delete = edit_delete
        mod.install_pip = install_pip
        mod.parse_pre = _format.parse_pre
        mod.edit_or_reply = edit_or_reply
        mod.logger = logging.getLogger(shortname)
        mod.borg = petercord
        spec.loader.exec_module(mod)
        # for imports
        sys.modules["pyPetercord.plugins." + shortname] = mod
        LOGS.info("Successfully imported " + shortname)


def remove_plugin(shortname):
    try:
        cmd = []
        if shortname in PLG_INFO:
            cmd += PLG_INFO[shortname]
        else:
            cmd = [shortname]
        for cmdname in cmd:
            if cmdname in LOADED_CMDS:
                for i in LOADED_CMDS[cmdname]:
                    petercord.remove_event_handler(i)
                del LOADED_CMDS[cmdname]
        return True
    except Exception as e:
        LOGS.error(e)
    try:
        for i in LOAD_PLUG[shortname]:
            petercord.remove_event_handler(i)
        del LOAD_PLUG[shortname]
    except BaseException:
        pass
    try:
        name = f"pyPetercord.plugins.{shortname}"
        for i in reversed(range(len(petercord._event_builders))):
            ev, cb = petercord._event_builders[i]
            if cb.__module__ == name:
                del petercord._event_builders[i]
    except BaseException:
        raise ValueError
