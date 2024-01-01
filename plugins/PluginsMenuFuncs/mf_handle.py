from models import Menu
from utils.PlugCtrl import PlugCtrl
from models import viewer

# from plugins.pluginMenu import _PluginMenuPlug


def scrollUp(menu: Menu.Menu):
    if menu.kwargs["__ItemPointer"] == 0:
        return "Up to top", None, 1
    menu.kwargs["__ItemPointer"] -= 1
    return "", None, viewer.RESSCR_ONLYMAINSCREEN


def scrollDown(menu: Menu.Menu):
    if menu.kwargs["__ItemPointer"] == len(PlugCtrl.PlugInfoList) - 1:
        return "Up to bottom", None, 1
    menu.kwargs["__ItemPointer"] += 1
    return "", None, viewer.RESSCR_ONLYMAINSCREEN


def exit(menu: Menu.Menu):
    return "", None, viewer.RESSCR_BACKMENU
