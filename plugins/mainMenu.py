from models.Manager import Manager
from config.EnvCfg import EnvCfg
from models import (
    ItemObj,
    Menu,
    TagContext,
    ControlContext,
    BasePlugin,
)
from utils.PlugCtrl import PlugCtrl
from plugins.mainMenuFuncs.rule import controlRule

# 显示函数区
# 被动显示
from plugins.mainMenuFuncs.pd_Display import (
    getCurrentDir,
    getListDir,
    getPageInfo,
    littleTip,
    supportedShortCut,
    getCurrentShortCut,
)


"""功能函数
接受参数(Description, func, shortCut, name). 其中func([1])成员接受一个Menu变量作为参数
功能函数需要对menu的相关成员进行修改，如调kwargs["ItemPointer"]或者对kwargs["manager"]按照kwargs["TagCtx"]进行某种修改
因为反馈到viewer只有字符串,新的菜单
返回值只接受(str|None,Menu|None,int)，Menu不为空则显示新的菜单,最后一个Int是resetCode

## 触发方式
viewer的listen函数循环接受到值后执行input传入栈顶的menu的Menu.input()
"""
"""主菜单的被动信息显示函数
- 获得当前路径某文件的具体信息
- 获得全部插件的基本信息(name+author)
- 获得某插件的具体信息
- 获得某功能的信息
"""


"""功能menufuncs
menufuncs的成员为(Description, func, shortCut, name). 其中func([1])成员接受一个Menu变量作为参数
功能函数需要对menu的相关成员进行修改，如调kwargs["ItemPointer"]或者对kwargs["manager"]按照kwargs["TagCtx"]进行某种修改
因为反馈到viewer只有字符串,新的菜单
返回值只接受(str|None,Menu|None,int)，Menu不为空则显示新的菜单，最后一个int是resetCode
以下定义func们
"""
# 功能-显示


# 功能-勾选


class __mainMenuPlug(BasePlugin.BasePlugin):
    def __init__(
        self,
        PluginName: str,
        Description: str = "",
        Author: str = "",
        Url: str = "",
        Version: str = "",
    ) -> None:
        super().__init__(PluginName, Description, Author, Url, Version)


__MainMenuPlug = __mainMenuPlug(
    PluginName="主菜单加载", Description="显示主菜单", Author="scarletborder", Version="0.0.1b"
)


def __initMainMenu(menu: Menu.Menu):
    manager = Manager("")  # 保证根目录和其下初始化过

    def initTagCtx(tagCtx: TagContext.TagContext, *args, **kwargs):
        items: list[ItemObj.ItemObj] = kwargs.get("itemobjs", [])
        l = len(items)
        for idx in range(l):
            tagCtx.setTagDetail(idx, {"type": items[idx].type}, True)
            tagCtx.setTagDetail(idx, items[idx].ExtraInfo, False)

    menu.tagCtx = TagContext.TagContext(
        len(manager.CurrentDir.contents),
        initTagCtx,
        itemobjs=manager.CurrentDir.contents,
    )
    menu.ControlCtx = ControlContext.ControlContext(controlRule)
    menu.displayFuncs = [
        getCurrentDir,
        getListDir,
        getPageInfo,
        littleTip,
        supportedShortCut,
        getCurrentShortCut,
    ]
    # 控制视图的参数

    menu.kwargs["__ItemPointer"] = 0  # 光标->文件/文件夹
    # _maxNumPerPage = len(CurrentDir.contents)  # 总共的条数 每次动态获得
    # 视图的全局项
    infoConfig = EnvCfg["info"]
    menu.kwargs["__BASEFUNCNUM"] = infoConfig.get("BaseFuncNum", 10)  # 基本行为(非插件)的数量
    menu.kwargs["__LINEPERPAGE"] = infoConfig.get("LinePerPage", 10)  # 每页资源管理器中显示的资源行数
    menu.kwargs["__LINEPERFOOT"] = infoConfig.get("LinePerFoot", 2)  # 脚注提示的快捷命令每行最大指令个数
    menu.kwargs["PreviewItemPreviousList"] = []
    menu.kwargs["PreviewItemAfterList"] = []
    menu.kwargs["manager"] = manager


def __prefixAndAfterPerLine(menu: Menu.Menu):
    def __defaultPrevious(*args) -> str:
        itemPtr = args[0]
        tagCtx: TagContext.TagContext = args[1]
        idx = args[2]
        line = ""
        if idx == itemPtr:
            line = ">\t"
        else:
            line = str(idx) + "\t"

        if tagCtx.getTagDetail(idx, "type", "File") == "dir":
            line += "[D]"
        return line

    def __defaultAfter(*args) -> str:
        itemPtr = args[0]
        tagCtx: TagContext.TagContext = args[1]
        idx = args[2]
        line = ""

        if tagCtx.getTagDetail(idx, "checked", False) is True:
            line += "[+]"
        else:
            line += "[ ]"
        return ""

    menu.kwargs["PreviewItemPreviousList"].append(__defaultPrevious)
    menu.kwargs["PreviewItemAfterList"].append(__defaultAfter)


__MainMenuPlug.regMenuInitFunc(__initMainMenu, 0)
__MainMenuPlug.regMenuInitFunc(__prefixAndAfterPerLine, 0)
__MainMenuPlug.regNewSupportExt(["pdf"])

# 功能区
from plugins.mainMenuFuncs.mf_extraInfo import (
    showFuncInfo,
    showItemDetail,
    showPluginInfo,
)
from plugins.mainMenuFuncs.mf_page import (
    openDir,
    backDir,
    scrollDown,
    scrollUp,
    scrollLeft,
    scrollRight,
    exitExec,
)

__MainMenuPlug.regNewMenuFunc(showFuncInfo, "显示指令描述", "q", "detail", 0)
__MainMenuPlug.regNewMenuFunc(openDir, "打开文件夹", "d", "openDir", 0)
__MainMenuPlug.regNewMenuFunc(backDir, "退出当前文件夹", "a", "exitDir", 0)
__MainMenuPlug.regNewMenuFunc(scrollDown, "", "j", "down", 0)
__MainMenuPlug.regNewMenuFunc(scrollUp, "", "k", "up", 0)
__MainMenuPlug.regNewMenuFunc(scrollLeft, "", "h", "left", 0)
__MainMenuPlug.regNewMenuFunc(scrollRight, "", "l", "right", 0)
__MainMenuPlug.regNewMenuFunc(exitExec, "退出程序", "ESC", "Exit", 0)
__MainMenuPlug.regNewMenuFunc(showItemDetail, "显示item详细描述", "f", "Info", 0)
__MainMenuPlug.regNewMenuFunc(showPluginInfo, "打开插件管理器", "p", "Plugs", 0)
# __MainMenuPlug.regNewFileConvert()

PlugCtrl.loadPlugin(__MainMenuPlug)
