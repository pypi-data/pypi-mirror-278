#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/12
# @Author  : alan
# @File    : setup.py
import os
import sys

from setuptools import find_packages, setup, Command
from shutil import rmtree

NAME = 'loggingA'
VERSION = '0.0.6'

here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git commit -am "Update version {0}"'.format(about['__version__']))
        os.system('git push')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name=NAME,  # 项目的名称，name是包的分发名称。独一无二
    version=about['__version__'],  # 项目的版本。需要注意的是，PyPI上只允许一个版本存在，如果后续代码有了任何更改，再次上传需要增加版本号
    author="alan",  # 项目作者的名字和邮件, 用于识别包的作者。
    author_email="al6nlee@gmail.com",
    description="自定义日志模块",  # 项目的简短描述
    long_description=long_description,  # 项目的详细描述，会显示在PyPI的项目描述页面。必须是rst(reStructuredText) 格式的
    long_description_content_type="text/markdown",
    url="https://github.com/al6nlee/loggingA",
    packages=find_packages(exclude=('tests', 'tests.*')),  # 指定最终发布的包中要包含的packages
    classifiers=[  # 其他信息，一般包括项目支持的Python版本，License，支持的操作系统
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development"
    ],
    install_requires=[],  # 项目依赖哪些库(内置库就可以不用写了)，这些库会在pip install的时候自动安装
    python_requires='>=3.8',
    license='MIT',
    package_data={  # 默认情况下只打包py文件，如果包含其它文件比如.so格式，增加以下配置
        "loggingA": [
            "*.py",
            "*.so",
        ]
    },
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,  # 运行 python3 setup.py upload 时，就会触发 UploadCommand 类的 run() 方法
    },
)
