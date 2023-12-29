"""资源管理器和插件管理
"""
from models.BasePlugin import BasePlugin
import os
from models import DirObj, TagContext, ItemObj, ControlContext
from utils.PlugCtrl import PlugCtrl


class PlugNotFoundError(Exception):
    def __init__(self, plugName) -> None:
        self.msg = "Plugin " + plugName + " not existed."


class Manager:
    def __init__(self, rp: str) -> None:
        # 文件管理
        if rp == "":
            __rootpath = os.getcwd().rsplit("\\", 1)
        else:
            __rootpath = rp.rsplit("\\", 1)
        self.CurrentDir = DirObj.DirObj(
            __rootpath[1], __rootpath[0], PlugCtrl.DirInitFuncs
        )  # 初始，指向RootDir
        self.initCurrentDirInfo()

    # PDF和文件夹的路径管理
    # def previousDir()
    def initCurrentDir(self):
        """初始化currentDir指向的DirObj本身"""
        for fun in PlugCtrl.DirInitFuncs:
            fun(self.CurrentDir)

    def initCurrentDirInfo(self):
        """初始化CurrentDir文件夹下的所有ItemObj"""
        self.CurrentDir.initInfo(
            PlugCtrl.supportExts, PlugCtrl.fileInitFuncs, PlugCtrl.DirInitFuncs
        )

    def backDir(self) -> bool:
        """CurrentDir指定到father Dir"""
        if self.CurrentDir.fatherPath.find("\\") == -1:
            return False
        olderpath = self.CurrentDir.fatherPath.rsplit("\\", 1)
        self.CurrentDir = DirObj.DirObj(olderpath[1], olderpath[0])
        self.initCurrentDirInfo()
        return True
