def controlRule(s: str) -> tuple[bool, str | None]:
    """快捷键匹配规则
    ## params
    - s: 需要判断的指令
    - return:
    |序号  |含义   |
    |---|---|
    |0   |is prefix of any command   |
    |1| if true, 指令的序号 or None(前缀而已尚未完全匹配),if false, None |
    """
    if s[0] == "q":
        prefixStatus = controlRule(s[1:])
        if prefixStatus[1] is not None:
            return True, "q"
        elif prefixStatus[0] == True:
            return True, None
        else:
            return False, None
    if s in {"d", "a", "j", "k", "h", "l", "f", "p", "!"}:
        return True, s
    else:
        return False, None
