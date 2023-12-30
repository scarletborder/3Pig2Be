"""将keyboard输入的单词转变为字符或大写字符或符号字符防止单词
目的是使得controlRule简单
符号不能是name如-=[] \\ ;',./`
转入 esc->!
转出 !->ESC
特殊键可以转换成符号或者大写字符，因为保证inp到rule中时正常键无大写或者符号
因为大写的单词序列不与shortCut(提示快捷键)的其他情况前缀重复
"""

__trans_in = {"esc": "!", "enter": "E"}

__trans_out = {"!": "ESC", "E": "ENTER"}


def inp(inp: str) -> str:
    """word输入转char"""
    return __trans_in.get(inp, inp)


def outp(s: str) -> str:
    """char输出转char或大写WORD"""
    ret = ""
    for c in s:
        ret += __trans_out.get(c, c)
    return ret


if __name__ == "__main__":
    import keyboard

    def pp(a: keyboard.KeyboardEvent):
        print(a)
        print(a.name)

    keyboard.hook(pp)
    keyboard.wait()
