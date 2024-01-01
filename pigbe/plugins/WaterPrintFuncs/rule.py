def __lowControlRule(s: str) -> tuple[bool, str | None]:
    """无q指令的Rule"""
    if s == "wd":
        return True, "wd"

    try:
        if "wd".index(s) == 0:
            return True, None
        else:
            return False, None
    except ValueError:
        return False, None


def mainMenuControlRule(s: str) -> tuple[bool, str | None]:
    if s[0] == "q":
        if len(s) == 1:
            return True, None
        status, idx = __lowControlRule(s[1:])
        if idx is not None:
            return True, "q"
        elif status is True:
            return True, None
        else:
            return False, None

    return __lowControlRule(s)


def watercontrolRule(s: str):
    """水印二级菜单
    快捷键匹配规则
    ## params
    - s: 需要判断的指令
    - return:
    |序号  |含义   |
    |---|---|
    |0   |is prefix of any command   |
    |1|if true, 指令的序号 or None(前缀而已尚未完全匹配) |
    """
    if s == "j":
        return True, "j"  # down
    elif s == "k":
        return True, "k"  # up
    elif s == "v":
        return True, "v"  # tick
    elif s == "w":
        return True, "w"  # del watermark by pix
    elif s == "e":
        return True, "e"  # del watermark and make watermark
    elif s == "s":
        return True, "s"
    elif s == "q":
        return True, "q"  # exit

    return False, None
