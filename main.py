import os
from Constant.config.EnvCfg import EnvCfg

# 检验更新
from utils import SoftWareInfo

# 加载插件
import plugins as _

# 加载viewer

from utils import viewer

if __name__ == "__main__":
    print(SoftWareInfo.getInfo())
    Viewer = viewer.Viewer()
    os.system("pause")
    Viewer.listen()
    # 加载主菜单
