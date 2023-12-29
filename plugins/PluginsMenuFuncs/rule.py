def controlRule(s: str):
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
    elif s == "!":
        return True, "!"  # exit

    return False, None
