import logging
from config.EnvCfg import EnvCfg

# 检验更新
logging.warning("当前无法检验程序是否为最新版，因为检验更新模块还没做好")
import plugins as _

# 加载viewer

from utils import viewer


Viewer = viewer.Viewer()

# 加载插件


if __name__ == "__main__":
    Viewer.listen()
    # 加载主菜单
