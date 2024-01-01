import os
from pigbe.plugins.WaterPrint import _WaterPrintDealPlug
from pigbe.models.Menu import Menu
from pigbe.models import TagContext
from pigbe.plugins.mainMenuFuncs.lib_check import (
    _delAllCheckedTag,
    _getAllCheckedTagItemPath,
)
from pigbe.utils.MenuMsgQueue import MenuMsgQueue


from pigbe.plugins.WaterPrintFuncs.rule import mainMenuControlRule, watercontrolRule
from pigbe.utils.combineContext import combineControlWithRule, combineTagContext
from pigbe.plugins.mainMenuFuncs.lib_check import (
    _getAllCheckedTagItemPath,
    _delAllFalseCheckedTag,
)

# 二级菜单
from pigbe.models.TagContext import TagContext
from pigbe.models.ControlContext import ControlContext
from pigbe.plugins.WaterPrintFuncs.pd_displayList import getListDir
from pigbe.plugins.WaterPrintFuncs.lib_delWater import (
    delWatermarkByPix,
    _getTmpDir,
    _addWaterMark,
)

ISDELSRC: bool = False
from pigbe.models import viewer

from pigbe.plugins.WaterPrintFuncs.config import WaterPrintPlugCfg


@_WaterPrintDealPlug.dregMenuInitFunc(2)
def initWaterMenuFunc(menu: Menu):
    menu.kwargs["contents"] = []
    MenuMsgQueue.getMsg(menu)

    for filePath in _getAllCheckedTagItemPath(menu.tagCtx):
        # 设置存储路径，将传入即将被删除水印的默认文件路径列表
        # 这个路径可以被另外的指令修改
        dst_filePath = filePath.rsplit("\\", 1)
        dst_filePath[1] = "whucao_" + dst_filePath[1]
        menu.tagCtx.setTagDetail(
            filePath, {"dst": dst_filePath[0] + "\\" + dst_filePath[1]}, False
        )
        # 设置追踪的文件名列表，方便统一序号
        menu.kwargs["contents"].append(filePath)

    menu.kwargs["ipointer"] = 0
    menu.displayFuncs.append(getListDir)


_WaterPrintDealPlug.addMenuControlRule(watercontrolRule, 2)


@_WaterPrintDealPlug.dregNewMenuFunc("测试勾选", "v", "Tick", 2)
def pressAndCheck(menu: Menu):
    """点一下勾选触发键的动作
    反选
    """
    # 获得选中项
    idx = menu.kwargs["contents"][menu.kwargs["ipointer"]]
    menu.tagCtx.setReverseCheck(idx, False)

    return "", None, viewer.RESSCR_ONLYMAINSCREEN


@_WaterPrintDealPlug.dregNewMenuFunc("", "j", "down", 2)
def scrollDown(menu: Menu):
    if menu.kwargs["ipointer"] == len(menu.kwargs["contents"]) - 1:
        return "Up to bottom", None, 1
    menu.kwargs["ipointer"] += 1
    return "", None, viewer.RESSCR_ONLYMAINSCREEN
    pass


@_WaterPrintDealPlug.dregNewMenuFunc("", "k", "up", 2)
def scrollUp(menu: Menu):
    if menu.kwargs["ipointer"] == 0:
        return "Up to top", None, 1
    menu.kwargs["ipointer"] -= 1
    return "", None, viewer.RESSCR_ONLYMAINSCREEN


@_WaterPrintDealPlug.dregNewMenuFunc("", "q", "exit", 2)
def exitWater(menu: Menu):
    # 同步tagCtx
    def __syncChecked(MainMenu: Menu):
        for filePath, checked in menu.tagCtx.getAllCheck(False).items():
            if checked is False:
                MainMenu.tagCtx.setCheck(filePath, False)
        _delAllFalseCheckedTag(MainMenu.tagCtx)

    MenuMsgQueue.sendMsg(__syncChecked, 0, 2)
    return "", None, viewer.RESSCR_BACKMENU


# 执行


@_WaterPrintDealPlug.dregNewMenuFunc("", "w", "delByPix", 2)
def _delWaterMarkByPix(menu: Menu):
    ret = []
    for filePath, istick in menu.tagCtx.getAllCheck().items():
        if istick is True:
            dstPath = menu.tagCtx.getTagDetail(filePath, "dst", None)
            if dstPath is not None:
                ret.append((filePath, dstPath))
    print("开始执行水印删除操作，通过图像处理\n")
    delWatermarkByPix(ret, isAdd=False, isdelsrc=ISDELSRC)

    def __delExistedTick(menu: Menu):
        _delAllCheckedTag(menu.tagCtx)

    MenuMsgQueue.sendMsg(__delExistedTick, 0, 2)
    return "处理完成", None, viewer.RESSCR_BACKMENU


@_WaterPrintDealPlug.dregNewMenuFunc("", "e", "Del&Add", 2)
def _delWaterMarkByPixandMark(menu: Menu):
    ret = []
    for filePath, istick in menu.tagCtx.getAllCheck().items():
        if istick is True:
            dstPath = menu.tagCtx.getTagDetail(filePath, "dst", None)
            if dstPath is not None:
                ret.append((filePath, dstPath))
    print("开始执行水印删除&添加操作，通过图像处理\n")
    delWatermarkByPix(ret, isAdd=True, isdelsrc=ISDELSRC)

    def __delExistedTick(menu: Menu):
        _delAllCheckedTag(menu.tagCtx)

    MenuMsgQueue.sendMsg(__delExistedTick, 0, 2)
    return "处理完成", None, viewer.RESSCR_BACKMENU


@_WaterPrintDealPlug.dregNewMenuFunc("", "s", "Add", 2)
def _AddWaterMark(menu: Menu):
    ret = []
    for filePath, istick in menu.tagCtx.getAllCheck().items():
        if istick is True:
            dstPath = menu.tagCtx.getTagDetail(filePath, "dst", None)
            if dstPath is not None:
                ret.append((filePath, dstPath))
    print("开始执行水印添加操作\n")
    for src, dst in ret:
        _addWaterMark(src, dst, isdelsrc=ISDELSRC)
        if os.path.exists(src) and menu.tagCtx.getTagDetail(
            "isDelSrc", "default", False
        ):
            os.remove(src)

    def __delExistedTick(menu: Menu):
        _delAllCheckedTag(menu.tagCtx)

    MenuMsgQueue.sendMsg(__delExistedTick, 0, 2)
    return "处理完成", None, viewer.RESSCR_BACKMENU


@_WaterPrintDealPlug.dregNewMenuFunc("切换是是否删除源文件", "z", "ifDelSrc", 2)
def _changeDelSrcMode(menu: Menu):
    global ISDELSRC
    if ISDELSRC is False:
        ISDELSRC = True
    else:
        ISDELSRC = False

    # setIsDel(originalMode)
    # menu.tagCtx.setTagDetail("isDelSrc", {"default": originalMode})

    return f"删除源文件已经切换为{ISDELSRC}", None, viewer.RESSCR_ALL
