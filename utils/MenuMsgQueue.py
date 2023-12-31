"""菜单之间传递信息"""
from models.Menu import Menu
import logging


class _menuMsgQueue:
    def __init__(self) -> None:
        # tuple[msg:str,rule:func,srcMenuId:int]
        self.__msgQueue: dict[int, list[tuple]] = dict()

    def sendMsg(self, rule, dstMenuId: int, srcMenuId: int = -1, msg: str = ""):
        """向管道中传递信息
        ## params
        - rule: 接受一个menu作为参数，为目标菜单根据信息如何更改的方法
        """

        oldList = self.__msgQueue.get(dstMenuId, [])
        oldList.append((msg, rule, srcMenuId))
        self.__msgQueue[dstMenuId] = oldList

    def getMsg(self, menu: Menu) -> list[str]:
        """菜单从管道中得到信息
        :returns - list[str]: 管道里的简讯
        """
        ret = []
        dstId = menu.getMenuId()
        l = self.__msgQueue.get(dstId, None)
        if l is not None:
            for msg, rule, srcId in l:
                rule(menu)
                ret.append(msg)
                logging.debug(msg + "from" + str(srcId))
            self.__msgQueue.pop(dstId)
        return ret


MenuMsgQueue = _menuMsgQueue()
