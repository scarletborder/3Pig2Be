import pkgutil

"""所有的插件一律为行为包，因为支持新类型总是有他的方法
插件继承于BasePlugin基类，初始化时执行其load方法
"""

__path__ = pkgutil.extend_path(__path__, __name__)
for imp, module, ispackage in pkgutil.walk_packages(
    path=__path__, prefix=__name__ + "."
):
    __import__(module)

"""menuID
- MainMenu: 0
- PluginList: 1
- ConvertMenu: 2
"""
