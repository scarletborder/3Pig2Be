"""一个menu所需要的子方法
- `pd_***.py`: 被动显示函数，在执行Menu.display()时显示，接受一个Menu参数，返回一个str。
- `mf_***.py`: 封装menuFunc，tuple类型，成员顺序(Description, func, shortCut, name)
    - func([1])成员接受一个Menu变量作为参数，同时返回回馈字符串""和二级菜单(Menu|None),resetCode
- `rule.py`: 快捷键规则，需要支持此级目录所有可能结果,一个函数，接受str作为参数，返回bool,int|None
- `lib_***.py`: 依赖，被子方法所调用  

## tips
### 如何重置规则
将原来的ContextRule作为成员，做个闭包
"""
