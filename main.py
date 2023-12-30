import os
from config.EnvCfg import EnvCfg

# 检验更新
from utils import SoftWareInfo

print(SoftWareInfo.getInfo())
import plugins as _

# 加载viewer

from utils import viewer


Viewer = viewer.Viewer()

# 加载插件


if __name__ == "__main__":
    os.system("pause")
    Viewer.listen()
    # 加载主菜单
