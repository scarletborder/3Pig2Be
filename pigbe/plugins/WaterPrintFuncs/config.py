import os

WaterPrintPlugCfg = {
    "dpi": 220,
    "tmp": os.path.dirname(__file__) + "/tmp",
    "core": 8,
    "MultiMethod": "spawn",
    "TopInfo": "WHUCAO 开源社区共享免费资料，遵循开源仓库知识共享协议，请勿以任何形式贩卖",
    "BottomInfo": "WHUCAO 开源社区:728342352",
    "RotateInfo": "WHUCAO 开源社区",
    "WaterMarkTemplate": os.path.dirname(__file__) + "/WaterMarkTemplate.pdf",
    # "WaterMarkTemplateL": os.path.dirname(__file__) + "/WaterMarkTemplateL.pdf",
    "rowsToDelete": [
        "满绩小铺QQ：1433397577，搜集整理不易，资料自用就好，谢谢！",
        "满绩小铺 QQ：1433397577，搜集整理不易，自用就好，请勿倒卖，谢谢！",
    ],
    "BigWaterMark": ["满绩小铺QQ：1433397577"],
}
if __name__ == "__main__":
    print(WaterPrintPlugCfg)
