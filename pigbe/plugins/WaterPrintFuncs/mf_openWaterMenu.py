from pigbe.plugins.WaterPrint import _WaterPrintDealPlug
from pigbe.models.Menu import Menu
from pigbe.plugins.mainMenuFuncs.lib_check import (
    _delAllCheckedTag,
    _getAllCheckedTagItemPath,
)
from pigbe.utils.MenuMsgQueue import MenuMsgQueue

from pigbe.models.TagContext import TagContext
from pigbe.plugins.WaterPrintFuncs.rule import mainMenuControlRule
from pigbe.utils.combineContext import combineControlWithRule, combineTagContext

from os.path import isdir, isfile
from os import scandir
from pigbe.models import viewer


@_WaterPrintDealPlug.dregNewMenuFunc("将勾选项带入水印(暂时只有，后续拓展)二级菜单", "wd", "delWaterMark", 0)
def enterDelWaterMenu(menu: Menu):
    if menu.tagCtx is not None:
        AlltickFileOrdir = _getAllCheckedTagItemPath(menu.tagCtx)  # 记录所有路径
        ret = []  # 只记录pdf

        def __recursivePDF(dirPath: str):
            nonlocal ret
            for filePath in scandir(dirPath):
                if filePath.path.count(".pdf") == 1 and filePath.is_file():
                    ret.append(filePath.path)
                elif filePath.path.count(".") == 0 and filePath.is_dir():
                    __recursivePDF(filePath.path)

        for filePath in AlltickFileOrdir:
            if filePath.count(".pdf") == 1 and isfile(filePath):
                ret.append(filePath)
            elif filePath.count(".") == 0 and isdir(filePath):
                # 文件夹filepath全部勾选，其下的所有pdf
                __recursivePDF(filePath)

        # del AlltickFileOrdir

        # 放入信息管道
        def __changeWaterMenuItem(menu: Menu):
            menu.tagCtx = combineTagContext(menu.tagCtx, TagContext(None))
            # 修改水印菜单初始的项目
            if menu.tagCtx is not None:
                for filePath in ret:
                    menu.tagCtx.setCheck(filePath, True, False)

        MenuMsgQueue.sendMsg(__changeWaterMenuItem, 2, 0)
        # num = _delAllCheckedTag(menu.tagCtx)
        return "使用JK上下移动,\nv勾选反选\nw执行清除水印\ns执行添加水印\ne执行清除&添加水印", Menu(2), 3
        # return f"{ret}\nhas already delete all {num} tick", Menu(2), 3
    return "此菜单缺失ControlContext", None, viewer.RESSCR_BACKMENU


@_WaterPrintDealPlug.dregMenuInitFunc(0)
def addWaterMenuEnter(menu: Menu):
    # 打开水印菜单的方法注册
    menu.ControlCtx = combineControlWithRule(menu.ControlCtx, mainMenuControlRule)
