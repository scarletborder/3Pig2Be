"""插件
# 插件编写指南
所有在插件包中通过注册函数注册的信息将被PlugCtrl获取
插件继承于BasePlugin基类，在插件main文件的最后需要显性地执行utils中PlugCtrl.loadPlugin()方法

## 文件命名暂行规范
- `pd_***.py`: 被动显示函数，在执行Menu.display()时显示，接受一个Menu参数，返回一个str。
- `mf_***.py`: 封装menuFunc，tuple类型，成员顺序(Description, func, shortCut, name)
    - func([1])成员接受一个Menu变量作为参数，同时返回回馈字符串""和二级菜单(Menu|None), resetCode
- `rule.py`: 快捷键规则，需要支持此级目录所有可能结果
- `lib_***.py`: 依赖，被子方法所调用 

## 允许注册的信息
除注册新的可支持拓展名为，其他注册函数都支持装饰器，@dreg***()，并在其下定义func参数函数
regNewSupportExt(self, extList: list):  注册新的可支持拓展名

regFileInit(self, ext: str, func):  注册跟踪文件对象初始化函数

regDirInit(self, func): 注册文件夹对象初始化函数
- ext: 处理的拓展名
- func: 接受一个DirObj作为参数的函数，并在DirObj.extraInfo添加相关信息
        
regNewFileConvert(self, srcExt: str, dstExt: str, Description, func): 注册文件转换功能
func需要支持接受FileObj和转化后的路径path作为参数
{"docx":[("pdf",func1)]}

 regNewMenuFunc(self, func, Description, shortCut: str, name: str, menuid: int): 拓展管理器行为
- func: 其中func成员接受一个Menu变量作为参数
- menuid: 被拓展的菜单id
        
regMenuInitFunc(self, func, menuid: int): 菜单初始化函数
- func: 以一个Menu变量作为参数，修改其属性
- menuid: 被修改的菜单id
        

## TagCtx
__init__(self, initRule, *args, **kwargs)

### initRule
初始化tag表的函数，接受需要初始化的TagCtx,*args,**kwargs作为参数

## ControlCtx
__init__(self, rule)

### rule
一个函数判断当前快捷键输入buffer的内容是否合法,传入str返回bool(是否是任何指令快捷键的前缀),idx(方法序号)

#### 如何重置规则
将原来的函数对象成员ContextRule作为一个前置判断条件，做个函数。如果是修改诸如连段规则如主菜单的q则还需再次指定q+新支持指令的规则

## 一些宏定义
### Viewer接受信号resetCode
重置命令行的等级
0 - 不重置
1 - 仅重置回馈字符串
2 - 仅重置主界面
3 - 都重置
4 - 向上级菜单返回

### menuID
- MainMenu: 0
- PluginList: 1
- ConvertMenu: 2
"""
import pkgutil


__path__ = pkgutil.extend_path(__path__, __name__)
for imp, module, ispackage in pkgutil.walk_packages(
    path=__path__, prefix=__name__ + "."
):
    if module.count(".") == 2:
        __import__(module)
