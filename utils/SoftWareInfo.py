import requests
from Constant.config.EnvCfg import EnvCfg
import yaml, logging


def startInfo() -> str:
    return (
        "=" * 5
        + EnvCfg["Global"]["Title"]
        + "=" * 5
        + "\nAuthor:"
        + EnvCfg["Global"]["Author"]
        + "\nUrl:"
        + EnvCfg["Global"]["url"]
        + "\nVersion:"
        + EnvCfg["Global"]["Version"]
        + "\n"
    )
    pass


def verifyUpdate() -> str:
    ret = ""
    url: str = EnvCfg["Global"]["Verify_Update"]
    if url == "":
        logging.warning(
            "Can not verify Main Branch version for the lost argument in config/config.yaml"
        )
    else:
        try:
            resp = requests.get(url=url, stream=True, timeout=3)
        except requests.exceptions.ConnectTimeout:
            logging.warning(f"无法在远端验证主分支版本，连接{url}超时")
        except BaseException as e:
            logging.warning("Unexpected Exception" + str(e))
        else:
            remoteCfg = yaml.safe_load(resp.text)
            if EnvCfg["Global"]["Version"] == remoteCfg["Global"]["Version"]:
                ret += f"你的版本已到达远端主分支版本\n"
            elif EnvCfg["Global"]["Version"] > remoteCfg["Global"]["Version"]:
                ret += f"你的版本新于远端主分支版本\n"
            else:
                ret += f"你的版本落后于远端主分支版本\n"

    url: str = EnvCfg["Global"]["Verify_Update_dev"]
    if url == "":
        logging.warning(
            "Can not verify Dev Branch version for the lost argument in config/config.yaml"
        )
    else:
        try:
            resp = requests.get(url=url, stream=True, timeout=3)
        except requests.exceptions.ConnectTimeout:
            logging.warning(f"无法在远端验证dev分支版本，连接{url}超时")
        except BaseException as e:
            logging.warning("Unexpected Exception" + str(e))
        else:
            remoteCfg = yaml.safe_load(resp.text)
            if EnvCfg["Global"]["Version"] == remoteCfg["Global"]["Version"]:
                ret += f"你的版本已到达远端dev分支版本\n"
            elif EnvCfg["Global"]["Version"] > remoteCfg["Global"]["Version"]:
                ret += f"你的版本新于远端dev分支版本\n"
            else:
                ret += f"你的版本落后于远端dev分支版本\n"
    return ret


def getInfo() -> str:
    return startInfo() + verifyUpdate()
