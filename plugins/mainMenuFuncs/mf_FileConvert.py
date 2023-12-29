"""文件转换功能
具有一个二级菜单，并且有勾选这个tag 
可以对所有被勾选的文件按照规则进行转换
二级菜单中将可以切换功能
指定目的格式/指定执行方法/指定路径(预留一个三级菜单功能)
"""
from models import DirObj, FileObj, ItemObj, ControlContext, TagContext, Manager


def convertFunc(items: list):
    """文件转换顶层功能"""
    # 文件转换只对fileobj起作用
    idx = 0
    for idx in range(len(items)):
        if type(items[idx]) == DirObj:
            items.pop(idx)
            continue
        idx += 1

    tagCtx = TagContext.TagContext(len(items))
    # 需要有支持转换的列表和方法

    def inner():
        pass


# def getSupportedConvertExt(menu: Menu.Menu):
#     """转移到功能
#     得到受支持转化后缀名列表"""
#     ret = []
#     manager : Manager= menu.kwargs["manager"]
#     manager.supportExts
# SupportedToExt = GlobalManager.fileConvertFuncs.get(self.type,[])
