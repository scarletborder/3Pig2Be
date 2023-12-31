from pigbe.models.TagContext import TagContext


def __clearTagCtxWithOnlyCheck(item: tuple):
    """删除只有Menu.TagCtx中只有Type,checked以及有ExtraInfo但是为空的item"""
    itemKey = item[0]
    itemValue = item[1]
    situation1 = set(itemValue.keys()).issubset(("Type", "checked"))
    situation2 = False
    if situation1 is not True:
        if set(itemValue.keys()).issubset(("Type", "checked", "ExtraInfo")):
            if len(itemValue.get("ExtraInfo", dict())) == 0:
                situation2 = True

    if situation1 or situation2:
        return True
    return False


def __clearTagCtxWithOnlyFalseCheck(item: tuple):
    """删除只有Menu.TagCtx中只有Type,checked(为false)以及有ExtraInfo但是为空的item"""
    itemKey = item[0]
    itemValue = item[1]

    if itemValue.get("checked", False) is True:
        return False

    situation1 = set(itemValue.keys()).issubset(("Type", "checked"))

    situation2 = False
    if situation1 is not True:
        if set(itemValue.keys()).issubset(("Type", "checked", "ExtraInfo")):
            if len(itemValue.get("ExtraInfo", dict())) == 0:
                situation2 = True

    if situation1 or situation2:
        return True
    return False


def _delAllCheckedTag(tagCtx: TagContext | None) -> int:
    if tagCtx is None:
        return 0
    return tagCtx.delItemWithRule(__clearTagCtxWithOnlyCheck)


def _delAllFalseCheckedTag(tagCtx: TagContext | None) -> int:
    if tagCtx is None:
        return 0
    return tagCtx.delItemWithRule(__clearTagCtxWithOnlyFalseCheck)


def _getAllCheckedTagItemPath(tagCtx: TagContext) -> list[str]:
    ret: list[str] = []
    for itemKey, value in tagCtx.getAllCheck().items():
        if value is True:
            ret.append(itemKey)
    return ret
