"""勾选"""
from models.Menu import Menu
from models.TagContext import TagContext

from plugins.mainMenu import _MainMenuPlug


@_MainMenuPlug.dregNewMenuFunc("反选光标项", "v", "Tick", 0)
def pressAndCheck(menu: Menu):
    """点一下勾选触发键的动作
    反选
    """
    # 获得选中项
    idx = (
        menu.kwargs["manager"]
        .CurrentDir.contents[menu.kwargs["__ItemPointer"]]
        .filePath
    )

    menu.tagCtx.setReverseCheck(idx, False)

    return "", None, 2


@_MainMenuPlug.dregMenuInitFunc(0)
def addSuffixToMainMenu(menu: Menu):
    def __itemTickBox(*args) -> str:
        # func(__ItemPointer, menu.tagCtx, idx)
        # ipointer : int= args[0]
        tagCtx: TagContext = args[1]
        idx = args[2]
        idx = menu.kwargs["manager"].CurrentDir.contents[idx].filePath
        isTick = tagCtx.getCheck(idx, False)
        if isTick is True:
            return "[+]"
        return "[ ]"

    menu.kwargs["PreviewItemSuffixList"].append(__itemTickBox)


# def clearTagCtxWithRule(menu: Menu):
#     """通过某种规则删除Menu.TagCtx的键值对"""
