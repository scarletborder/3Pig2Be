class ItemObj(object):
    """跟踪item基类"""

    def __init__(self, name, fatherPath: str, type: str) -> None:
        self.fatherPath = fatherPath
        self.Name = name
        self.type = type
        self.filePath = ""
        self.ExtraInfo = dict()  # 额外信息，默认支持的有是否被勾选。可被插件进行修改
