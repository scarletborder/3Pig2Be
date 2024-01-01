from models import Menu
from plugins.MainMenu import _MainMenuPlug
from utils.handleChar import outp
from models import viewer

# 一些功能回显字符串


def __getItemDetail(menu: Menu.Menu, idx: int) -> str:
    """获得当前路径序号文件的具体信息
    ## params
    - return: 如果idx越界返回`None`，否则
    |params|description|type|必须|
    |---|---|---|---|
    |Name|跟踪item的名称|str|是|
    |FilePath|文件路径|str|是|
    |Chosen|是否勾选|bool|否|
    |ExtraInfo|插件规定的额外信息|dict|是|
    """
    if menu.tagCtx is not None:
        # if idx >= menu.tagCtx.getOptionNums():
        #     return "No found idx"
        item = menu.kwargs["manager"].CurrentDir.contents[idx]
        return str(item.Name) + str(menu.tagCtx.getTagAllDetail(item.filePath))
    return ""


# def getMenuFuncInfo(menu: Menu.Menu):
#     idx: int = menu.kwargs["__ItemPointer"]
#     if idx >= len(menu.kwargs["manager"].managerFuncs):
#         return "No found idx"
#     return str(menu.menuFuncs[idx][3]) + str(menu.menuFuncs[idx][0]), None, 3


@_MainMenuPlug.dregNewMenuFunc("显示item详细描述", "f", "Info", 0)
def showItemDetail(menu: Menu.Menu):
    return (
        __getItemDetail(menu=menu, idx=menu.kwargs["__ItemPointer"]),
        None,
        viewer.RESSCR_ONLYCALLBACK,
    )


@_MainMenuPlug.dregNewMenuFunc("显示指令描述", "q", "detail", 0)
def showFuncInfo(menu: Menu.Menu):
    """得到某功能的具体信息"""
    if menu.ControlCtx is not None:
        isLaw, idx = menu.ControlCtx._rule(menu.ControlCtx.getCurrentShortCut()[1:])
        if idx is not None and isLaw is True:
            idx = outp(idx)
            return menu.menuFuncs[idx][3] + ":" + menu.menuFuncs[idx][0], None, 1
        return "", None, viewer.RESSCR_ONLYCALLBACK
    return "此菜单缺失ControlContext", None, 4
