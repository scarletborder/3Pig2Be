from models.Manager import Manager
from models import DirObj, FileObj, ItemObj
from config.EnvCfg import EnvCfg
import logging
import os

# 初始化，根目录


# 处理页数


"""与内容无关的行为，如展示信息之类的
"""


def getAllFunc():
    # 展示所有可用行为
    ret: list[str] = []
    idx = 0
    for intro in GlobalManager.fileFuncs:
        ret.append(str(idx) + intro[0])
        idx += 1
    return ret


# 行为执行
def execFunc(idx: int):
    """根据所选值执行行为
    - idx: 所选择的行为
    """
    if idx >= __BASEFUNCNUM:
        # 拓展行为
        GlobalManager.fileFuncs[idx - __BASEFUNCNUM][1]
    else:
        # 根据序号选
        pass
    pass
