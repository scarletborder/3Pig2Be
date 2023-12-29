"""
根据行为对文件夹对象进行处理
"""

from models import DirObj, Menu, TagContext, ItemObj
import logging
from utils.PlugCtrl import PlugCtrl


# 基本行为(非插件)，如打开，翻页，勾选等
# 对mainMenu进行特化

# 同步tagCtx和extrainfo

"""打开/回退
在opendir和backdir中，每次新建一个list(dir)存放已经跟踪的文件/夹，
检查当前目录下的文件是否在这个list中，没有的话初始化加入
"""


def __initTagCtx(tagCtx: TagContext.TagContext, *args, **kwargs):
    items: list[ItemObj.ItemObj] = kwargs.get("itemobjs", [])
    l = len(items)
    for idx in range(l):
        tagCtx.setTagDetail(idx, {"type": items[idx].type}, True)
        tagCtx.setTagDetail(idx, items[idx].ExtraInfo, False)


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
        menu.tagCtx = TagContext.TagContext(
            len(menu.kwargs["manager"].CurrentDir.contents),
            __initTagCtx,
            itemobjs=menu.kwargs["manager"].CurrentDir.contents,
        )
        return "", None, 3


def backDir(menu: Menu.Menu):
    status = menu.kwargs["manager"].backDir()
    if status is True:
        menu.kwargs["__ItemPointer"] = 0
        menu.tagCtx = TagContext.TagContext(
            len(menu.kwargs["manager"].CurrentDir.contents),
            __initTagCtx,
            itemobjs=menu.kwargs["manager"].CurrentDir.contents,
        )
        return "", None, 3
    else:
        return "已到根目录下", None, 1


"""翻页"""


def scrollDown(menu: Menu.Menu):
    if (
        menu.kwargs["__ItemPointer"]
        == len(menu.kwargs["manager"].CurrentDir.contents) - 1
    ):
        return "Up to bottom", None, 1
    menu.kwargs["__ItemPointer"] += 1
    return "", None, 2
    pass


def scrollUp(menu: Menu.Menu):
    if menu.kwargs["__ItemPointer"] == 0:
        return "Up to top", None, 1
    menu.kwargs["__ItemPointer"] -= 1
    return "", None, 2


def scrollLeft(menu: Menu.Menu):
    lev = int(menu.kwargs["__ItemPointer"] / menu.kwargs["__LINEPERPAGE"])
    if lev == 0:
        return "Up to top", None, 1
    else:
        menu.kwargs["__ItemPointer"] -= menu.kwargs["__LINEPERPAGE"]
        return "", None, 2


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
        return "", None, 2


def exitExec(menu: Menu.Menu):
    return "", None, 4


# 在选择中，多项选择会涉及到上翻页和下翻页，自动忽略文件夹
# 当然目前版本不支持v num G
