from models import Menu
from plugins.mainMenu import _MainMenuPlug
from utils.handleChar import outp

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
    # if idx >= menu.tagCtx.getOptionNums():
    #     return "No found idx"
    item = menu.kwargs["manager"].CurrentDir.contents[idx]
    return str(item.Name) + str(menu.tagCtx.getTagAllDetail(item.filePath))


# def getMenuFuncInfo(menu: Menu.Menu):
#     idx: int = menu.kwargs["__ItemPointer"]
#     if idx >= len(menu.kwargs["manager"].managerFuncs):
#         return "No found idx"
#     return str(menu.menuFuncs[idx][3]) + str(menu.menuFuncs[idx][0]), None, 3


@_MainMenuPlug.dregNewMenuFunc("显示item详细描述", "f", "Info", 0)
def showItemDetail(menu: Menu.Menu):
    return __getItemDetail(menu=menu, idx=menu.kwargs["__ItemPointer"]), None, 1


@_MainMenuPlug.dregNewMenuFunc("显示指令描述", "q", "detail", 0)
def showFuncInfo(menu: Menu.Menu):
    """得到某功能的具体信息"""
    isLaw, idx = menu.ControlCtx._rule(menu.ControlCtx.getCurrentShortCut()[1:])
    if idx is not None and isLaw is True:
        idx = outp(idx)
        return menu.menuFuncs[idx][3] + ":" + menu.menuFuncs[idx][0], None, 1
    return "", None, 1


@_MainMenuPlug.dregNewMenuFunc("打开插件管理器", "p", "Plugs", 0)
def showPluginInfo(menu: Menu.Menu):
    """从主菜单打开一个插件列表二级菜单"""
    return "使用JK上下移动\nq键退出", Menu.Menu(1), 3
