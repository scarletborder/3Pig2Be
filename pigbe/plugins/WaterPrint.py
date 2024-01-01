from pigbe.models.BasePlugin import BasePlugin
from pigbe.models.Menu import Menu
from pigbe.models import ControlContext
from pigbe.utils.PlugCtrl import PlugCtrl

# MenuId of new menu
WATERPRINT_MENUID = 2


class __waterPrintDealer(BasePlugin):
    pass


_WaterPrintDealPlug = __waterPrintDealer(
    "水印处理", "对PDF文件的水印做出一系列处理\n，目前只支持删除功能", "scarletborder", "", "0.0.2d"
)

import pigbe.plugins.WaterPrintFuncs.mf_water as _
import pigbe.plugins.WaterPrintFuncs.mf_openWaterMenu as _


PlugCtrl.loadPlugin(_WaterPrintDealPlug)
# def getItemExtraInfo(item, attr: str, default):
#     """获得item的额外信息，如果该信息不存在，那么将Defalut赋值给他并返回"""
#     if attr in item.__dict__:
#         return item.__dict__[attr]
#     elif "ExtraInfo" in item.__dict__:
#         if attr not in item.ExtraInfo.keys():
#             item.ExtraInfo[attr] = default
#         return item.ExtraInfo.get(attr, default)
#     else:
#         return None


# """全局行为"""


# def delFilesWaterPrint(fileObjs: list[FileObj.FileObj]):
#     # 处置已经处理删除水印的对象
#     length = len(fileObjs)
#     idx = 0
#     while idx < length:
#         if getItemExtraInfo(fileObjs[idx], "hasWaterPrint", True) is False:
#             fileObjs.pop(idx)
#             length -= 1
#         else:
#             idx += 1


# """初始化fileobj(参数只允许有一个FileObj)"""


# def addWaterPrintAttrs(fileObj: FileObj.FileObj):
#     if fileObj.type == "md":
#         fileObj.ExtraInfo["hasWaterPrint"] = False
#     else:
#         fileObj.ExtraInfo["hasWaterPrint"] = True


# """
# 加载
# """
# FileObj.FileInitAddons.append(addWaterPrintAttrs)
