from setuptools import setup, find_packages
from Constant.config.EnvCfg import EnvCfg

setup(
    name=EnvCfg["Global"]["Name"],
    version=EnvCfg["Global"]["Version"],
    packages=find_packages(),
    entry_points={"console_scripts": ["pigbe=pigbe.main:main_func"]},
    author="scarletborder",
    description=EnvCfg["Global"]["Description"],
    install_requires=[
        " keyboard>=0.13.5",
        "PyMuPDF>=1.22.5",
        "PyPDF2>=3.0.1",
        "PyYAML>=6.0.1",
        "PyYAML>=6.0.1",
        "Requests>=2.31.0",
    ],
)
