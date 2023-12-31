from utils.combineContext import combineControlWithRule


class BasePlugin(object):
    def __init__(
        self,
        PluginName: str,
        Description: str = "",
        Author: str = "",
        Url: str = "",
        Version: str = "0.0.0",
    ) -> None:
        # info
        self.PluginName = PluginName
        self.Description = Description
        self.Author = Author
        self.Url = Url
        self.Version = Version
        # addons
        self.menuInitAddons: list[tuple] = list()
        self.menuFuncAddons: list[tuple[int, tuple]] = []  # 在菜单中出现，做出某种行为如对勾选文件处理或者展示信息
        self.supportExtsAddons: list[str] = []
        self.fileInitAddons: list[tuple] = []  # {"docx":[func1,func2]}
        self.fileConvertFuncs: list[
            tuple
        ] = []  # {"docx":{"pdf":[(desp,func1), (desp,func2)] }}
        self.dirInitAddons: list = []

        pass

    def regNewSupportExt(self, extList: list):
        """注册新的可支持拓展名"""
        self.supportExtsAddons += extList

    def regFileInit(self, ext: str, func):
        """注册跟踪文件对象初始化函数
        # params
        - ext: 处理的拓展名
        - func: 接受一个FileObj作为参数的函数，并在FileObj.extraInfo添加相关信息
        """
        self.fileInitAddons.append((ext, func))

    def dregFileInit(self, ext: str):
        """装饰器注册跟踪文件对象初始化函数
        # params
        - ext: 处理的拓展名
        - func: 接受一个FileObj作为参数的函数，并在FileObj.extraInfo添加相关信息
        """

        def inner(func):
            self.regFileInit(ext, func)

        return inner

    def regDirInit(self, func):
        """注册文件夹对象初始化函数
        # params
        - ext: 处理的拓展名
        - func: 接受一个DirObj作为参数的函数，并在DirObj.extraInfo添加相关信息
        """
        self.fileInitAddons.append(func)

    def dregDirInit(self):
        """注册文件夹对象初始化函数
        # params
        - ext: 处理的拓展名
        - func: 接受一个DirObj作为参数的函数，并在DirObj.extraInfo添加相关信息
        """

        def inner(func):
            self.regDirInit(func)

        return inner

    def regNewFileConvert(self, srcExt: str, dstExt: str, Description, func):
        """注册文件转换功能
        func需要支持接受FileObj和转化后的路径path作为参数
        {"docx":[("pdf",func1)]}"""
        self.fileConvertFuncs.append((srcExt, dstExt, (Description, func)))

    def dregNewFileConvert(self, srcExt: str, dstExt: str, Description):
        """注册文件转换功能
        func需要支持接受FileObj和转化后的路径path作为参数
        {"docx":[("pdf",func1)]}"""

        def inner(func):
            self.regNewFileConvert(srcExt, dstExt, Description, func)

        return inner

    def regNewMenuFunc(self, func, Description, shortCut: str, name: str, menuid: int):
        """拓展管理器行为
        # params
        - func: 其中func成员接受一个Menu变量作为参数
        - menuid: 被拓展的菜单id
        """
        self.menuFuncAddons.append((menuid, (Description, func, shortCut, name)))

    def dregNewMenuFunc(self, Description, shortCut: str, name: str, menuid: int):
        """拓展管理器行为
        # params
        - func: 其中func成员接受一个Menu变量作为参数
        - menuid: 被拓展的菜单id
        """

        def inner(func):
            self.regNewMenuFunc(func, Description, shortCut, name, menuid)

        return inner

    def regMenuInitFunc(self, func, menuid: int):
        """菜单初始化函数
        - func: 以一个Menu变量作为参数，修改其属性
        - menuid: 被修改的菜单id
        """
        self.menuInitAddons.append((menuid, func))

    def dregMenuInitFunc(self, menuid: int):
        """菜单初始化函数
        - func: 以一个Menu变量作为参数，修改其属性
        - menuid: 被修改的菜单id
        """

        def inner(func):
            self.regMenuInitFunc(func, menuid)

        return inner

    def addMenuControlRule(self, rule, menuId: int):
        """增加控制函数
        传入str返回bool(是否是任何指令快捷键的前缀),idx(方法序号)
        """

        def __addRule(menu):
            menu.ControlCtx = combineControlWithRule(menu.ControlCtx, rule)

        self.regMenuInitFunc(__addRule, menuId)

    def daddMenuControlRule(self, menuId: int):
        def inner(func):
            self.addMenuControlRule(func, menuId)

        return inner
