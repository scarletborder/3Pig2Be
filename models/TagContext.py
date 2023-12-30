import logging


class TagContext:
    """用来给菜单的选项打tag的
    ## params
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

    def __init__(self, initRule, *args, **kwargs) -> None:
        # self.__optionNums = optionNums
        self.__store: dict[str, dict] = dict()
        initRule(self, *args, **kwargs)  # 进行如ExtraInfo同步等初始化操作
        pass

    # def getOptionNums(self):
    #     return self.__optionNums

    def setTagDetail(self, itemKey: str, newDict: dict, overRide: bool = False):
        # if itemKey >= self.__optionNums:
        #     logging.error(
        #         "missing idx", str(itemKey), "max number is ", str(self.__optionNums)
        #     )
        #     return
        if overRide is True:
            oldDict = newDict
        else:
            oldDict = self.__store.get(itemKey, dict())
            oldDict.update(newDict)
        self.__store[itemKey] = oldDict
        return oldDict

    def setTagDetailWithRule(self, itemKey: str, rule, overRide: bool = False):
        """通过规则得到字典改变tag上下文
        ## params
        - rule: 规则，接受单条项目的字典dict作为参数，返回新字典
        - overRide:
            - False: 用通过规则生成的某条项目新字典更新原字典
            - True:用新的某条项目的字典替换旧的某条项目字典
        """
        # if itemKey >= self.__optionNums:
        #     logging.error(
        #         "missing idx", str(itemKey), "max number is ", str(self.__optionNums)
        #     )
        #     return
        oldDict = self.__store.get(itemKey, dict())
        newDict = rule(oldDict)
        if overRide is True:
            oldDict = newDict
        else:
            oldDict = self.__store.get(itemKey, dict())
            oldDict.update(newDict)
        self.__store[itemKey] = oldDict
        return oldDict

    def setCheck(self, itemKey: str, isCheck: bool, overRide: bool = False):
        self.setTagDetail(itemKey, {"checked": isCheck}, overRide=overRide)

    def setReverseCheck(self, itemKey: str, overRide: bool = False):
        def reverse(tagDict: dict) -> dict:
            checked = tagDict.get("checked", False)
            if checked is True:
                tagDict["checked"] = False
            else:
                tagDict["checked"] = True
            return tagDict

        return self.setTagDetailWithRule(itemKey, reverse, overRide)

    def getTagAttrs(self, itemKey: str):
        # if itemKey >= self.__optionNums:
        #     logging.error(
        #         "missing idx", str(itemKey), "max number is ", str(self.__optionNums)
        #     )
        #     return None
        return self.__store.get(itemKey, dict()).keys()

    def getTagAllDetail(self, itemKey: str):
        """得到单条项目的所有属性的字典"""
        # if itemKey >= self.__optionNums:
        #     logging.error(
        #         "missing idx", str(itemKey), "max number is ", str(self.__optionNums)
        #     )
        #     return None
        return self.__store.get(itemKey, dict())

    def getTagDetail(self, itemKey: str, tagKey: str, default):
        # if itemKey >= self.__optionNums:
        #     logging.error(
        #         "missing idx", str(itemKey), "max number is ", str(self.__optionNums)
        #     )
        #     return None
        tagDict = self.__store.get(itemKey, dict())
        return tagDict.get(tagKey, default)

    def getCheck(self, itemKey: str, default: bool = False):
        return self.getTagDetail(itemKey, "checked", default)

    def getAllTagDetail(self, tagKey: str, default) -> dict:
        """得到所有项目的某属性dict[str,Any]"""
        ret = dict()
        # for itemKey in range(self.__optionNums):
        #     ret.append(self.getTagDetail(itemKey, tag, default))
        for itemKey in self.__store.keys():
            ret[itemKey] = self.getTagDetail(itemKey, tagKey, default)
        return ret

    def getAllCheck(self):
        """dict[str,bool]"""
        return self.getAllTagDetail("checked", False)
