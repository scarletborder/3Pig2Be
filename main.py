import argparse, sys, os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from pigbe.Constant.config.EnvCfg import EnvCfg
from pigbe.utils.myLogger import Logger

# 检验更新
from pigbe.utils import SoftWareInfo

# 加载插件
from pigbe.models import viewer


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

    Logger.info(SoftWareInfo.getInfo(args.check_version))
    import pigbe.plugins as _

    os.system("pause")

    # 加载viewer
    Viewer = viewer.Viewer(EnvCfg["Launch"]["InitialMenuId"])

    Viewer.listen()


if __name__ == "__main__":
    main_func()
