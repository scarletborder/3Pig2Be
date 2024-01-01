import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="3Pig2Be",
        description="A complex tool powered by various plugins to process file.",
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
    from Constant.config.EnvCfg import EnvCfg

    Logger.info(SoftWareInfo.getInfo(args.check_version))

    os.system("pause")

    # 加载viewer
    Viewer = viewer.Viewer(EnvCfg["Launch"]["InitialMenuId"])

    Viewer.listen()
    # 加载主菜单
