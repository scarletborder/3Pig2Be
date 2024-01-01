"""控制的配置
在一个Context中支持的命令
"""
from utils.handleChar import outp


class ControlContext:
    def __init__(self, rule):
        """
        :rule - 一个函数判断当前快捷键输入buffer的内容是否合法,传入str返回bool(是否可以继续输入),idx(方法序号)
        """
        self.__currentShortCut: str = ""
        self._rule = rule

    def input(self, inp: str) -> str | None:
        """键入字母
        整行效果
        如果有执行或者无法识别效果那么clear并执行"""
        self.__currentShortCut += inp
        # 判断是否合法的目前键入字母
        status, idx = self._rule(self.__currentShortCut)
        if status is True:  # 匹配到
            if idx is not None:
                return idx
        else:  # 不存在于任何前缀
            self.clear()
        return

    def clear(self):
        self.__currentShortCut = ""

    def getCurrentShortCut(self):
        """目前正在输入的快捷键"""
        return self.__currentShortCut

    def getShortCutStr(self) -> str:
        """字符串形式"""
        return self.getCurrentShortCut()

    def getRealShortCutStr(self) -> str:
        """获得实际的输入(特殊键将转换为大写WORD)，如esc键为ESC而不再是!"""
        return outp(self.getCurrentShortCut())

    def getRule(self):
        return self._rule

    def changeRule(self, rule):
        self._rule = rule


"""
        # 判断是否合法的目前键入字母
        allPrefix = self.__rule.keys()
        # 仅判断这个最后一位
        pos = len(self.__currentShortCut) - 1  
        status = False
        for wd in allPrefix:
            if len(wd) < pos + 1:
                continue
            else:
                if wd[pos] == inp:
                    # 存在前缀
                    status = True
                    if len(wd) == pos + 1:
                        # 发现
                        return self.__rule[self.__currentShortCut]

        if status is False:
            self.clear()
"""
