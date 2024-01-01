"""
CLI视觉效果
"""
import keyboard
from models import Menu
import os, sys
from utils import handleChar, MenuMsgQueue

# enum
RESSCR_NONE = 0
RESSCR_ONLYCALLBACK = 1
RESSCR_ONLYMAINSCREEN = 2
RESSCR_ALL = 3
RESSCR_BACKMENU = 4


class Viewer:
    """视图
    管理菜单输入输出"""

    def __init__(self, MenuId: int) -> None:
        self.ShiftDown = False
        self.MenuStack: list[Menu.Menu] = [Menu.Menu(MenuId)]
        self.menuScreen: str = ""
        self.recallBuffer: str = ""
        self.resetCode: int = 3
        pass

    def readKey(self, keyEvent: keyboard.KeyboardEvent):
        name = keyEvent.name
        """特殊名称转换()除了shift)"""
        name = handleChar.inp(str(name))

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

    def forward(self, reMenu: Menu.Menu):
        MenuMsgQueue.MenuMsgQueue.getMsg(reMenu)
        self.MenuStack.append(reMenu)

    def back(self):
        if len(self.MenuStack) == 1:
            keyboard.press("ESC")
            sys.exit(0)
        else:
            self.MenuStack.pop()
            MenuMsgQueue.MenuMsgQueue.getMsg(self.MenuStack[-1])
        pass

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
            self.back()

        if self.resetCode == 1 or self.resetCode == 3 or self.resetCode == 4:
            self.recallBuffer = recallBuffer

        if reMenu is not None:
            self.forward(reMenu)

        self.setDisplayMain()
        self.setDisplayRecall()
        self.Display()

    def setDisplayMain(self):
        """展示menu被动界面"""
        if self.resetCode == 2 or self.resetCode == 3 or self.resetCode == 4:
            self.menuScreen = self.MenuStack[-1].display()
        return

    def setDisplayRecall(self):
        """展示menu回馈字符串"""
        return

    def Display(self):
        os.system("cls")
        print(
            "\n", self.menuScreen, "\n", "=" * 10, "\n", self.recallBuffer, flush=True
        )

    def listen(self):
        keyboard.hook(self.readKey)
        self.setDisplayMain()
        self.Display()
        keyboard.wait("ESC")
