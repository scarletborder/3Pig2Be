import logging


class TagContext:
    """用来给菜单的选项打tag的
    ## params
    - optionNums: 被打tag的项目个数
    - initRule: 初始化tag表的函数，接受TagCtx,*args,**kwargs作为参数
    - *args: 初始化项目tag用
    ## method
    - `setTagDetail( )`: 设置详细属性(增加或覆盖)
    - `setTagDetailWithRule( )`: 通过规则设置属性(增加或覆盖)
    - `setCheck( )`: 设置勾选tag
    - `setReverseCheck( )`: 设置反转勾选tag
    - `getTagAttrs( )`: 得到属性种类列表
    - `getTagDetail`( ): 详细属性
    - `getCheck( )`: 勾选属性
    - `getAllTagDetail( )`: 得到所有项目的某个详细属性[]
    - `getAllCheck( )`: 得到所有项目的勾选属性(默认支持的一个tag)[True,False]
    ## 使用场景
    1. 如勾选项
    2. 二级菜单配置某些细节。
    """

    def __init__(self, optionNums: int, initRule, *args, **kwargs) -> None:
        self.__optionNums = optionNums
        self.__store: dict[int, dict] = dict()
        initRule(self, *args, **kwargs)  # 进行如ExtraInfo同步等初始化操作
        pass

    def getOptionNums(self):
        return self.__optionNums

    def setTagDetail(self, opt: int, tagInfo: dict, overRide: bool = False):
        if opt >= self.__optionNums:
            logging.error(
                "missing idx", str(opt), "max number is ", str(self.__optionNums)
            )
            return
        if overRide is True:
            tagDict = tagInfo
        else:
            tagDict = self.__store.get(opt, dict())
            tagDict.update(tagInfo)
        self.__store[opt] = tagDict

    def setTagDetailWithRule(self, opt: int, rule, overRide: bool = False):
        if opt >= self.__optionNums:
            logging.error(
                "missing idx", str(opt), "max number is ", str(self.__optionNums)
            )
            return
        tagDict = self.__store.get(opt, dict())
        newDict = rule(tagDict)
        if overRide is True:
            tagDict = newDict
        else:
            tagDict = self.__store.get(opt, dict())
            tagDict.update(newDict)
        self.__store[opt] = tagDict

    def setCheck(self, opt: int, isCheck: bool, overRide: bool = False):
        self.setTagDetail(opt, {"checked": isCheck}, overRide=overRide)

    def setReverseCheck(self, opt: int, overRide: bool = False):
        def reverse(tagDict: dict) -> dict:
            checked = tagDict.get("checked", False)
            if checked is True:
                tagDict["checked"] = False
            else:
                tagDict["checked"] = True
            return tagDict

        self.setTagDetailWithRule(opt, reverse, overRide)

    def getTagAttrs(self, opt: int):
        if opt >= self.__optionNums:
            logging.error(
                "missing idx", str(opt), "max number is ", str(self.__optionNums)
            )
            return None
        return self.__store.get(opt, dict()).keys()

    def getTagAllDetail(self, opt: int):
        if opt >= self.__optionNums:
            logging.error(
                "missing idx", str(opt), "max number is ", str(self.__optionNums)
            )
            return None
        return self.__store.get(opt, dict())

    def getTagDetail(self, opt: int, tag: str, default):
        if opt >= self.__optionNums:
            logging.error(
                "missing idx", str(opt), "max number is ", str(self.__optionNums)
            )
            return None
        tagDict = self.__store.get(opt, dict())
        return tagDict.get(tag, default)

    def getCheck(self, opt: int):
        return self.getTagDetail(opt, "checked", False)

    def getAllTagDetail(self, tag: str, default):
        ret = []
        for opt in range(self.__optionNums):
            ret.append(self.getTagDetail(opt, tag, default))

    def getAllCheck(self):
        return self.getAllTagDetail("checked", False)
