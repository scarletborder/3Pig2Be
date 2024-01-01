import argparse, sys, os
from Constant.config.EnvCfg import EnvCfg

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def main_func():
    parser = argparse.ArgumentParser(
        prog=EnvCfg["Global"]["Name"],
        description=EnvCfg["Global"]["Description"],
    )
    parser.add_argument(
        "--check-version",
        help="Check version of program before start",
        action="store_true",
    )
    args = parser.parse_args()
    import os
    from utils.myLogger import Logger

    # 检验更新
    from utils import SoftWareInfo

    # 加载插件
    import plugins as _
    from models import viewer

    Logger.info(SoftWareInfo.getInfo(args.check_version))

    os.system("pause")

    # 加载viewer
    Viewer = viewer.Viewer(EnvCfg["Launch"]["InitialMenuId"])

    Viewer.listen()


if __name__ == "__main__":
    main_func()
