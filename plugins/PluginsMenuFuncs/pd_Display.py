"""
被动展示所有插件
"""

from models.Menu import Menu
from models.BasePlugin import BasePlugin
from utils.PlugCtrl import PlugCtrl


# 插件
def getAllPluginBrief(menu: Menu) -> str:
    """获得插件name-author简略信息
    展开__ItemPointer处的信息
    """
    ret = ""

    for i in range(len(PlugCtrl.PlugInfoList)):
        if i == menu.kwargs["__ItemPointer"]:
            ret += (
                "<"
                + PlugCtrl.PlugInfoList[i].get("PluginName", "NoName")
                + "-"
                + PlugCtrl.PlugInfoList[i].get("Version", "0.0.0")
                + ">\nAuthor:"
                + PlugCtrl.PlugInfoList[i].get("Author", "anonymous")
                + "\n描述:"
                + PlugCtrl.PlugInfoList[i].get("Description", "no description here")
                + "\nURL:"
                + PlugCtrl.PlugInfoList[i].get("Url", "no url here")
                + "\n"
            )
        else:
            ret += (
                "["
                + PlugCtrl.PlugInfoList[i].get("PluginName", "NoName")
                + "-"
                + PlugCtrl.PlugInfoList[i].get("Version", "0.0.0")
                + "]\n"
            )
    return ret
