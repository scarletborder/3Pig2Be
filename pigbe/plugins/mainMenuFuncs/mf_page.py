"""
根据行为对文件夹对象进行处理
"""

from pigbe.models import Menu
from pigbe.plugins.mainMenuFuncs.models import DirObj, ItemObj
from pigbe.utils.PlugCtrl import PlugCtrl
from pigbe.plugins.mainMenu import _MainMenuPlug, _mainMenuTagCtxInitRule
from pigbe.models import viewer

# 基本行为(非插件)，如打开，翻页，勾选等
# 对mainMenu进行特化

# 同步tagCtx和extrainfo

"""打开/回退
在opendir和backdir中，每次新建一个list(dir)存放已经跟踪的文件/夹，
检查当前目录下的文件是否在这个list中，没有的话初始化加入
"""


# def __initTagCtx(tagCtx: TagContext.TagContext, *args, **kwargs):
#     items: list[ItemObj.ItemObj] = kwargs.get("itemobjs", [])
#     # l = len(items)
#     for item in items:
#         tagCtx.setTagDetail(item.filePath, {"type": item.type}, False)
#         tagCtx.setTagDetail(item.filePath, item.ExtraInfo, False)


@_MainMenuPlug.dregNewMenuFunc("打开文件夹", "d", "openDir", 0)
def openDir(menu: Menu.Menu):
    if (
        menu.kwargs["manager"].CurrentDir.contents[menu.kwargs["__ItemPointer"]].type
        != "dir"
    ):
        return "无法打开文件作为路径", None, 1
    else:
        menu.kwargs["manager"].CurrentDir = DirObj.DirObj(
            menu.kwargs["manager"]
            .CurrentDir.contents[menu.kwargs["__ItemPointer"]]
            .Name,
            menu.kwargs["manager"].CurrentDir.filePath,
            PlugCtrl.DirInitFuncs,
        )
        menu.kwargs["__ItemPointer"] = 0
        menu.kwargs["manager"].initCurrentDirInfo()
        # menu.tagCtx = TagContext.TagContext(
        #     # len(menu.kwargs["manager"].CurrentDir.contents),
        #     _mainMenuTagCtxInitRule,
        #     itemobjs=menu.kwargs["manager"].CurrentDir.contents,
        # )
        return "", None, viewer.RESSCR_ALL


@_MainMenuPlug.dregNewMenuFunc("退出当前文件夹", "a", "exitDir", 0)
def backDir(menu: Menu.Menu):
    status = menu.kwargs["manager"].backDir()
    if status is True:
        menu.kwargs["__ItemPointer"] = 0
        # menu.tagCtx = TagContext.TagContext(
        #     # len(menu.kwargs["manager"].CurrentDir.contents),
        #     _mainMenuTagCtxInitRule,
        #     itemobjs=menu.kwargs["manager"].CurrentDir.contents,
        # )
        return "", None, 3
    else:
        return "已到根目录下", None, viewer.RESSCR_ONLYCALLBACK


"""翻页"""


@_MainMenuPlug.dregNewMenuFunc("", "j", "down", 0)
def scrollDown(menu: Menu.Menu):
    if (
        menu.kwargs["__ItemPointer"]
        == len(menu.kwargs["manager"].CurrentDir.contents) - 1
    ):
        return "Up to bottom", None, 1
    menu.kwargs["__ItemPointer"] += 1
    return "", None, viewer.RESSCR_ONLYMAINSCREEN
    pass


@_MainMenuPlug.dregNewMenuFunc("", "k", "up", 0)
def scrollUp(menu: Menu.Menu):
    if menu.kwargs["__ItemPointer"] == 0:
        return "Up to top", None, 1
    menu.kwargs["__ItemPointer"] -= 1
    return "", None, viewer.RESSCR_ONLYMAINSCREEN


@_MainMenuPlug.dregNewMenuFunc("", "h", "left", 0)
def scrollLeft(menu: Menu.Menu):
    lev = int(menu.kwargs["__ItemPointer"] / menu.kwargs["__LINEPERPAGE"])
    if lev == 0:
        return "Up to top", None, 1
    else:
        menu.kwargs["__ItemPointer"] -= menu.kwargs["__LINEPERPAGE"]
        return "", None, viewer.RESSCR_ONLYMAINSCREEN


@_MainMenuPlug.dregNewMenuFunc("", "l", "right", 0)
def scrollRight(menu: Menu.Menu):
    if int(menu.kwargs["__ItemPointer"] / menu.kwargs["__LINEPERPAGE"]) * menu.kwargs[
        "__LINEPERPAGE"
    ] + menu.kwargs["__LINEPERPAGE"] >= len(menu.kwargs["manager"].CurrentDir.contents):
        return "Up to bottom", None, 1
    else:
        menu.kwargs["__ItemPointer"] = (
            int(menu.kwargs["__ItemPointer"] / menu.kwargs["__LINEPERPAGE"] + 1)
            * menu.kwargs["__LINEPERPAGE"]
        )
        return "", None, viewer.RESSCR_ONLYMAINSCREEN


@_MainMenuPlug.dregNewMenuFunc("退出程序", "ESC", "Exit", 0)
def exitExec(menu: Menu.Menu):
    return "", None, viewer.RESSCR_BACKMENU


# 在选择中，多项选择会涉及到上翻页和下翻页，自动忽略文件夹
# 当然目前版本不支持v num G
