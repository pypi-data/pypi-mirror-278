"""
@Time    : 2024/6/11 20:07
@Author  : LuTuo
@report :allure generate ./report -o reports --clean
@pyinstaller -F -i img.ico .py
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="utilsLuTuo",                               # 包名
    version="1.0",                                 # 版本号
    author="LuTuo",                                     # 作者
    author_email="1803228677@qq.com",                        # 邮箱
    description="luTuoTest",                      # 简短描述
    long_description=long_description,               # 详细说明
    long_description_content_type="text/markdown",   # 详细说明使用标记类型
    packages=find_packages(where="src"),             # 需要打包的部分
    package_dir={"": "src"},                         # 设置src目录为根目录
    python_requires=">=3.6",                         # 项目支持的Python版本
    include_package_data=False                       # 是否包含非Python文件（如资源文件）
)
