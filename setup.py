from setuptools import setup, find_packages
from pigbe.Constant.config.EnvCfg import EnvCfg

# import sys, os

# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
setup(
    name=EnvCfg["Global"]["Name"],
    version=EnvCfg["Global"]["Version"],
    packages=find_packages(),
    entry_points={"console_scripts": ["pigbe=pigbe.__main__:main_func"]},
    author="scarletborder",
    description=EnvCfg["Global"]["Description"],
    install_requires=[
        "keyboard>=0.13.5",
        "PyMuPDF>=1.22.5",
        "PyPDF2>=3.0.1",
        "PyYAML>=6.0.1",
        "PyYAML>=6.0.1",
        "Requests>=2.31.0",
    ],
    exclude_package_data={"": ["__pycache__"]},
    include_package_data=True,
    zip_safe=True,
)
