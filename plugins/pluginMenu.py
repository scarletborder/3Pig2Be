from models.BasePlugin import BasePlugin
from models.Menu import Menu
from models import ControlContext

from plugins.PluginsMenuFuncs.pd_Display import getAllPluginBrief
from plugins.PluginsMenuFuncs import mf_handle, rule

from utils.PlugCtrl import PlugCtrl


class __pluginList(BasePlugin):
    def __init__(
        self,
        PluginName: str,
        Description: str = "",
        Author: str = "",
        Url: str = "",
        Version: str = "",
    ) -> None:
        super().__init__(PluginName, Description, Author, Url, Version)

    pass


__PluginMenuPlug = __pluginList("插件列表", "展示你安装的所有插件", "scarletborder", "", "0.0.1a")


def __initPluginMenu(menu: Menu):
    menu.displayFuncs = [getAllPluginBrief]
    menu.ControlCtx = ControlContext.ControlContext(rule.controlRule)
    menu.kwargs["__ItemPointer"] = 0


__PluginMenuPlug.regMenuInitFunc(__initPluginMenu, 1)
__PluginMenuPlug.regNewMenuFunc(mf_handle.scrollUp, "", "k", "up", 1)
__PluginMenuPlug.regNewMenuFunc(mf_handle.scrollDown, "", "j", "down", 1)
__PluginMenuPlug.regNewMenuFunc(mf_handle.exit, "", "ESC", "exit", 1)

PlugCtrl.loadPlugin(__PluginMenuPlug)
