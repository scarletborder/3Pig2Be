"""
CLI视觉效果
"""
import keyboard
from models import Menu
import os, sys


class Viewer:
    def __init__(self) -> None:
        self.ShiftDown = False
        self.MenuStack: list[Menu.Menu] = [Menu.Menu(0)]
        self.menuScreen: str = ""
        self.recallBuffer: str = ""
        self.resetCode: int = 3
        pass

    def readKey(self, keyEvent: keyboard.KeyboardEvent):
        name = keyEvent.name
        """特殊名称转换()除了shift)"""
        if name == "esc":
            name = "!"

        if keyEvent.event_type == "down":
            if keyEvent.name == "shift":
                self.ShiftDown = True
            else:
                if self.ShiftDown is True:
                    self.input(f"^{name}")

                else:
                    self.input(str(name))

        else:
            if keyEvent.name == "shift":
                self.ShiftDown = False

    def input(self, inp: str):
        recallBuffer, reMenu, self.resetCode = self.MenuStack[-1].input(inp)
        """resetCode
        重置命令行的等级
        0 - 不重置
        1 - 仅重置回馈字符串
        2 - 仅重置主界面
        3 - 都重置
        4 - 向上级菜单返回
        """
        if self.resetCode == 4:
            if len(self.MenuStack) == 1:
                sys.exit()
            else:
                self.MenuStack.pop()

        if self.resetCode == 1 or self.resetCode == 3 or self.resetCode == 4:
            self.recallBuffer = recallBuffer

        if reMenu is not None:
            self.MenuStack.append(reMenu)
        self.displayMain()
        self.displayRecall()

    def displayMain(self):
        """展示menu被动界面"""
        if self.resetCode == 2 or self.resetCode == 3 or self.resetCode == 4:
            self.menuScreen = self.MenuStack[-1].display()
        os.system("cls")
        print("\n", self.menuScreen)

    def displayRecall(self):
        """展示menu回馈字符串"""
        print("\n", "=" * 10)
        print(self.recallBuffer)

    def listen(self):
        keyboard.hook(self.readKey)
        self.displayMain()
        keyboard.wait()