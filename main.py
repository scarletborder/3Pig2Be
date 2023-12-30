import os
from config.EnvCfg import EnvCfg

# 检验更新
from utils import SoftWareInfo
import sys


print(SoftWareInfo.getInfo())
# 加载插件
import plugins as _

# 加载viewer

from utils import viewer

if __name__ == "__main__":
    Viewer = viewer.Viewer()
    os.system("pause")
    Viewer.listen()
    # 加载主菜单
