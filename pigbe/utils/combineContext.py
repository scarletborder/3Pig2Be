"""组合"""
"""组合两个TagContext"""
from pigbe.models.TagContext import TagContext
from pigbe.models.ControlContext import ControlContext


def combineTagContext(a: TagContext | None, b: TagContext):
    if a is None:
        return b
    else:
        return a.combineTagContext(b)


"""组合ControlContext.ControlRule
一个函数判断当前快捷键输入buffer的内容是否合法,传入str返回bool(是否是任何指令快捷键的前缀),idx(方法序号)
将原来的函数对象成员ContextRule作为一个前置判断条件，做个函数
"""


def combineControlWithRule(ctx: ControlContext | None, rule2) -> ControlContext:
    """Context组合一个新规则
    ## params
    - ctx: 原先的ctx，可能是空(menu没有初始化)
    - rule2: 后来的规则
    """
    if ctx is None:
        return ControlContext(rule2)

    rule1 = ctx.getRule()

    def ret(s: str) -> tuple[bool, int | None]:
        status, idx = rule1(s)
        # storageStatus = status
        if idx is not None:
            return True, idx
        elif status is True:
            status, idx = rule2(s)
            if idx is not None:
                return True, idx
            else:
                return True, None
        else:
            # 第一个规则失效
            return rule2(s)

    ctx.changeRule(ret)
    return ctx
