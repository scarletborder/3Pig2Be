from models.BasePlugin import BasePlugin


class plugCtrl:
    def __init__(self) -> None:
        self.PlugInfoList: list[dict[str, str]] = []
        self.supportExts: set[str] = set()
        self.fileInitFuncs: dict[str, list] = dict()  # {"docx":[func1,func2]}
        self.fileConvertFuncs: dict[  # 文件转化功能,例如["docx":[("pdf",func1)]]
            str, dict[str, list]
        ] = dict()  # {"docx":{"pdf":[func1, func2] }}
        self.DirInitFuncs = []
        self.menuFuncs: dict[int, list[tuple]] = dict()
        self.menuInitFuncs: dict[int, list] = dict()
        pass

    def getSupportExts(self):
        return self.supportExts

    def getFileInitFuncs(self):
        return self.fileInitFuncs

    def getFileConvertFuncs(self):
        return self.fileConvertFuncs

    def getDirInitFuncs(self):
        return self.DirInitFuncs

    def getMenuFuncs(self, menuID: int):
        return self.menuFuncs[menuID]

    def getMenuInitFuncs(self, menuID: int):
        return self.menuInitFuncs[menuID]

    def loadPlugin(self, Plugin: BasePlugin):
        # 注册信息
        self.PlugInfoList.append(
            {
                "PluginName": Plugin.PluginName,
                "Description": Plugin.Description,
                "Author": Plugin.Author,
                "Url": Plugin.Url,
            }
        )

        # 放入对应的Addons到相应的容器里
        for ext in Plugin.supportExtsAddons:
            self.supportExts.add(ext)
        for item in Plugin.fileInitAddons:
            ext = item[0]
            func = item[1]
            tmpList = self.fileInitFuncs.get(ext, [])
            tmpList.append(func)
            self.fileInitFuncs[ext] = tmpList
        for item in Plugin.fileConvertFuncs:
            srcExt = item[0]
            dstExt = item[1]
            func = item[2]  # tuple 介绍+函数(只接受一个FileObj)
            tmpList = self.fileConvertFuncs.get(srcExt, {dstExt: []})
            dstList = tmpList.get(dstExt, [])
            dstList.append(func)
            tmpList[dstExt] = dstList
            self.fileConvertFuncs[srcExt] = tmpList
        self.DirInitFuncs += Plugin.dirInitAddons
        for item in Plugin.menuFuncAddons:
            tmpList = self.menuFuncs.get(item[0], [])
            tmpList.append(item[1])
            self.menuFuncs[item[0]] = tmpList  # 拓展功能
        for item in Plugin.menuInitAddons:
            tmpList = self.menuInitFuncs.get(item[0], list())
            tmpList.append(item[1])
            self.menuInitFuncs[item[0]] = tmpList


PlugCtrl = plugCtrl()
