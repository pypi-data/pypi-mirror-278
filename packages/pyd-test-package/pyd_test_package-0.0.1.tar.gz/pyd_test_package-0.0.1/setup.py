# Designer:Yudong Pan
# Coder:God's hand
# Time:2024/6/8 18:36
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# with open('requirements.txt', "r", encoding="utf-8") as f:
#     required = f.read().splitlines()

setup(
    name="pyd_test_package",  # 包名
    version="0.0.1",  # 版本号
    author="pyd",  # 作者
    author_email="panydacademy@163.com",  # 邮箱
    description="package test",  # 简短描述
    long_description=long_description,  # 详细说明
    long_description_content_type="text/markdown",  # 详细说明使用标记类型
    # url="https://github.com/",                     # 项目主页
    packages=find_packages(where="pyd_test_package"),  # 需要打包的部分
    package_dir={"": "pyd_test_package"},  # 设置pyd_test_package目录为根目录
    python_requires=">=3.6",  # 项目支持的Python版本
    # install_requires=required,                     # 项目必须的依赖
    include_package_data=False  # 是否包含非Python文件（如资源文件）
)
