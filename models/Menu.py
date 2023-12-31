from models import DirObj, FileObj, ItemObj, ControlContext, TagContext, Manager
from utils.PlugCtrl import PlugCtrl
from utils.handleChar import outp


class Menu:
    def __init__(self, menuId: int) -> None:
        """菜单
        ## params
        - displayFuncs: 这个菜单被执行显示函数时的一系列需要显示的字符串，接受一个Menu变量作为参数，返回一个str
        - menuFuncs: (Description, func, shortCut, name).
            - func([1])成员接受一个Menu变量作为参数，同时返回回馈字符串""和二级菜单(Menu|None), resetCode
        - kwargs: 一般包含需要追踪的项目,一些参数，如list[itemObj]，ItemPointer，用途:menuFuncs的Menu参数中顺便传入
        """
        self.__menuId = menuId
        self.tagCtx: TagContext.TagContext | None = None
        self.ControlCtx: ControlContext.ControlContext | None = None
        self.displayFuncs: list = []
        self.menuFuncs: dict[str, tuple] = dict()
        self.kwargs: dict = dict()
        for func in PlugCtrl.getMenuInitFuncs(menuID=menuId):
            func(self)

        for func in PlugCtrl.getMenuFuncs(menuID=menuId):
            self.menuFuncs[func[2]] = func

    def display(self) -> str:
        """展示菜单"""
        ret = ""
        for func in self.displayFuncs:
            ret += func(self) + "\n"
        return ret

    def input(self, inp: str) -> tuple:
        if self.ControlCtx is None:
            return "此菜单缺失ControlContext无法输入", None, 4
        idx = self.ControlCtx.input(inp)
        if idx is not None:
            idx = outp(idx)
            ret = self.menuFuncs[idx][1](self)
            self.ControlCtx.clear()  # 防止一些功能要读取快捷键缓冲区，延后clear
            return ret
        return ("", None, 3)  # 默认没有执行任何方式后的返回值

    def getMenuId(self) -> int:
        return self.__menuId
