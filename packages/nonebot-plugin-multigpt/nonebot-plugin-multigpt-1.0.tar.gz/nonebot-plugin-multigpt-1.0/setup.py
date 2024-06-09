import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.0'
DESCRIPTION = 'a python package for multiGPT,多模态ai工具'
LONG_DESCRIPTION = '基于Nonebot2平台，一个多模态AI聊天插件 能够识图，制作PPT，一键生成论文word文档，绘画，以及基本的对话功能'

# Setting up
setup(
    name="nonebot_plugin_multigpt",
    version=VERSION,
    author="syagina",
    author_email="3173707804@qq.com",
    description=DESCRIPTION,
    long_description_content_type="text",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python','GPT','ppt','word','docx','image','ai'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)