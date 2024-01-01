def __lowControlRule(s: str) -> tuple[bool, str | None]:
    """无q指令的Rule"""
    if s in {"p"}:
        return True, s
    else:
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
    pass


def plugListcontrolRule(s: str):
    """快捷键匹配规则
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
    elif s == "q":
        return True, "q"  # exit

    return False, None
