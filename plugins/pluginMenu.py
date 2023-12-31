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


_PluginMenuPlug = __pluginList("插件列表", "展示你安装的所有插件", "scarletborder", "", "0.0.2a")


def __initPluginMenu(menu: Menu):
    menu.displayFuncs = [getAllPluginBrief]
    menu.ControlCtx = ControlContext.ControlContext(rule.plugListcontrolRule)
    menu.kwargs["__ItemPointer"] = 0


_PluginMenuPlug.regMenuInitFunc(__initPluginMenu, 1)

from utils.combineContext import combineControlWithRule
from plugins.PluginsMenuFuncs.rule import mainMenuControlRule


@_PluginMenuPlug.dregMenuInitFunc(0)
def newMainMenuControlRule(menu: Menu):
    menu.ControlCtx = combineControlWithRule(menu.ControlCtx, mainMenuControlRule)


_PluginMenuPlug.regNewMenuFunc(mf_handle.scrollUp, "", "k", "up", 1)
_PluginMenuPlug.regNewMenuFunc(mf_handle.scrollDown, "", "j", "down", 1)
_PluginMenuPlug.regNewMenuFunc(mf_handle.exit, "", "q", "exit", 1)


@_PluginMenuPlug.dregNewMenuFunc("打开插件管理器", "p", "Plugs", 0)
def showPluginInfo(menu: Menu):
    """从主菜单打开一个插件列表二级菜单"""
    return "使用JK上下移动\nq键退出", Menu(1), 3


PlugCtrl.loadPlugin(_PluginMenuPlug)
