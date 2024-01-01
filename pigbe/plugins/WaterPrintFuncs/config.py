import os

WaterPrintPlugCfg = {
    "dpi": 220,
    "tmp": os.path.dirname(__file__) + "/tmp",
    "TopInfo": "WHUCAO 开源社区共享免费资料，遵循开源仓库知识共享协议，请勿以任何形式贩卖",
    "BottomInfo": "WHUCAO 开源社区:728342352",
    "RotateInfo": "WHUCAO 开源社区",
    "WaterMarkTemplate": os.path.dirname(__file__) + "/WaterMarkTemplate.pdf",
}
if __name__ == "__main__":
    print(WaterPrintPlugCfg)
