import os
from plugins.mainMenuFuncs.models import FileObj
from plugins.mainMenuFuncs.models import ItemObj


class DirObj(ItemObj.ItemObj):
    def __init__(
        self,
        dirName: str,
        fatherPath: str,
        DirInitFuncs: list = [],
    ) -> None:
        """初始化跟踪文件夹对象"""
        super().__init__(dirName, fatherPath, "dir")
        self.contents: list[ItemObj.ItemObj] = []
        self.filePath = self.getDirPath()
        # InitAddons
        for func in DirInitFuncs:
            func(self)
        pass

    def getDirPath(self) -> str:
        return self.fatherPath + "\\" + self.Name

    def getFileNameList(self) -> list[str]:
        return [_.Name for _ in self.contents]

    def getFilePathList(self) -> list[str]:
        return [_.filePath for _ in self.contents]

    def initInfo(self, supportExts: set, fileInitFuncs: dict, dirInitFuncs: list):
        """首次被访问，对其下文件/文件夹进行初始化信息"""
        self.contents.clear()
        dirList = os.scandir(self.filePath)
        for item in dirList:
            if item.is_dir():
                self.contents.append(DirObj(item.name, self.filePath, dirInitFuncs))
                pass
            elif item.is_file():
                tempFileObj = FileObj.FileObj(
                    item.name, self.filePath, supportExts, fileInitFuncs
                )
                if tempFileObj.access is True:
                    self.contents.append(tempFileObj)
                pass
