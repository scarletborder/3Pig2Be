from models.Manager import Manager
from models import ItemObj, Menu, TagContext

"""主菜单的被动信息函数
    原生环境下支持以下方面的方法
    1. 资源管理器
        - 获得当前路径的基本信息
        - 获得当前路径全部文件的信息
        - 获得页数信息
    3. 脚注
        - 支持的快捷键-name
        - 正在输入的键
"""


def getCurrentDir(menu: Menu.Menu):
    """获得当前路径的基本信息"""
    return menu.kwargs["manager"].CurrentDir.filePath


def getHeader(menu: Menu.Menu):
    return "idx\tType\tName\tTick"


def getListDir(menu: Menu.Menu):
    """获得当前路径某页全部item的信息"""
    PreviewItemPrefixList = menu.kwargs["PreviewItemPrefixList"]
    __ItemPointer: int = menu.kwargs["__ItemPointer"]
    PreviewItemSuffixList = menu.kwargs["PreviewItemSuffixList"]
    __LINEPERPAGE: int = menu.kwargs["__LINEPERPAGE"]
    manager: Manager = menu.kwargs["manager"]

    ## 展示文件/文件夹 名前缀、后缀的内容
    def __previewItemPrevious(item: ItemObj.ItemObj, idx: int) -> str:
        line = ""
        for func in PreviewItemPrefixList:
            line += func(__ItemPointer, menu.tagCtx, idx, item) + "\t"  # 暂时不再添加额外的信息
        return line

    def __previewItemAfter(item: ItemObj.ItemObj, idx: int) -> str:
        line = ""
        for func in PreviewItemSuffixList:
            line += func(__ItemPointer, menu.tagCtx, idx, item) + "\t"  # 暂时不再添加额外的信息
        return line

    ret = ""
    page = int(__ItemPointer / __LINEPERPAGE)
    begin = page * __LINEPERPAGE
    end = min(len(manager.CurrentDir.contents), (page + 1) * __LINEPERPAGE)
    for idx in range(begin, end):
        item = manager.CurrentDir.contents[idx]
        prefix = __previewItemPrevious(item, idx)
        after = __previewItemAfter(item, idx)
        ret += f"{prefix}{item.Name}\t\t{after}\n"
        idx += 1
    return ret


def getPageInfo(menu: Menu.Menu) -> str:
    """获得页数信息"""
    __ItemPointer: int = menu.kwargs["__ItemPointer"]
    __LINEPERPAGE: int = menu.kwargs["__LINEPERPAGE"]
    manager: Manager = menu.kwargs["manager"]
    allItemNum = len(manager.CurrentDir.contents)
    if __LINEPERPAGE == -1:
        return "0/0(has shown all)"
    pages = int(allItemNum / __LINEPERPAGE) - 1
    if allItemNum % __LINEPERPAGE != 0:
        pages += 1
    page = int(__ItemPointer / __LINEPERPAGE)
    return f"{page}/{pages}(h-left,l-right)"


def littleTip(menu: Menu.Menu) -> str:
    return "q + 主页快捷键 可查看帮助"


def supportedShortCut(menu: Menu.Menu) -> str:
    """获得受支持的快捷键-name"""
    # manager = menu.kwargs["manager"]
    __LINEPERFOOT = menu.kwargs["__LINEPERFOOT"]

    ret = ""
    idx = 0
    for item in menu.menuFuncs.values():
        shortcuts = item[2]
        name = item[3]
        scStr = ""
        for k in shortcuts:
            if k == "shift":
                scStr += "^"
            else:
                scStr += str(k)
        ret += "{:<16}".format(scStr + " " + name)
        idx += 1
        if idx == __LINEPERFOOT:
            idx = 0
            ret += "\n"

    return ret


def getCurrentShortCut(menu: Menu.Menu):
    """目前正在输入的快捷键"""
    return menu.ControlCtx.getShortCutStr()
