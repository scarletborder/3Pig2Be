from pigbe.models import Menu


def getListDir(menu: Menu.Menu) -> str:
    """获得当前路径某页全部item的信息"""
    # PreviewItemPrefixList = menu.kwargs["PreviewItemPrefixList"]
    __ItemPointer: int = menu.kwargs["ipointer"]
    TickedInfo = menu.tagCtx.getAllTagDetail("checked", False)
    # PreviewItemSuffixList = menu.kwargs["PreviewItemSuffixList"]
    # __LINEPERPAGE: int = menu.kwargs["__LINEPERPAGE"]
    # manager: Manager = menu.kwargs["manager"]

    # ## 展示文件/文件夹 名前缀、后缀的内容
    # def __previewItemPrevious(item: ItemObj.ItemObj, idx: int) -> str:
    #     line = ""
    #     for func in PreviewItemPrefixList:
    #         line += func(__ItemPointer, menu.tagCtx, idx) + "\t"  # 暂时不再添加额外的信息
    #     return line

    # def __previewItemAfter(item: ItemObj.ItemObj, idx: int) -> str:
    #     line = ""
    #     for func in PreviewItemSuffixList:
    #         line += func(__ItemPointer, menu.tagCtx, idx) + "\t"  # 暂时不再添加额外的信息
    #     return line

    ret = ""
    # page = int(__ItemPointer / __LINEPERPAGE)
    # begin = page * __LINEPERPAGE
    # end = min(len(manager.CurrentDir.contents), (page + 1) * __LINEPERPAGE)
    idx = 0
    for filePath in menu.kwargs["contents"]:
        isTick = TickedInfo.get(filePath, False)
        if idx == __ItemPointer:
            prefix = ">"
        else:
            prefix = " "
        if isTick is True:
            suffix = "[+]"
        else:
            suffix = "[ ]"
        ret += f"{prefix}\t{filePath}\t\t{suffix}\n"
        idx += 1
    return ret
