import logging
from models import ItemObj
import os

# from models.DirObj import DirObj


class FileObj(ItemObj.ItemObj):
    """跟踪文件对象"""

    def __init__(
        self, fileName: str, fatherPath: str, supportExts: set, FileInitFuncs: dict
    ) -> None:
        ext = fileName.rsplit(".", 1)[-1]
        super().__init__(fileName, fatherPath, ext)
        self.filePath = fatherPath + "\\" + fileName

        # 可被操作性
        self.access = False
        if ext not in supportExts:
            logging.warning(f"File {self.filePath} 的拓展名尚不支持")

        else:
            self.access = True
            # InitAddons
            funcList = FileInitFuncs.get(self.type, [])
            for func in funcList:
                func(self)

        pass

    def convert(
        self,
        dstExt: str,
        idx: int,
        renameFunc,
        isDel: bool = False,
        fileConvertFuncs: dict = {},
    ) -> bool:
        """根据给定的支持转化
        ## brief
        一般是在外部维护一张srcExt->dstExt的表

        并且指定了固定的某srcExt的转换方法
        ## params
        - idx: 指定dstExt的转换方法
        - renameFunc: func(FileObj)->src，得到新文件的地址路径
        - isDel: 是否在转换完成后删除原文件
        """
        srcExt = self.type
        supportedExt = fileConvertFuncs.get(self.type, dict())
        convList = supportedExt.get(dstExt, [])
        if idx >= len(convList):
            logging.error(
                f"""{self.Name}: 拓展名{self.type}转化为{dstExt}只有{len(convList)}种方法，而你选择了第{idx}(+1)项"""
            )
            return False
        else:
            newPath = renameFunc(self)
            if newPath == self.filePath:
                logging.error(f"{self.filePath}目标路径和源路径重复")
                return False

            convList[idx][1](self, newPath)
            if isDel is True:
                os.remove(self.filePath)
            return True
