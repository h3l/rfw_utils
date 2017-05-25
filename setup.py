from setuptools import setup, find_packages
import sys, os
"""
打包的用的setup必须引入
"""

VERSION = '0.0.1'

with open('README.md') as f:
    long_description = f.read()


setup(
      name='rfw_utils', # 文件名
      version=VERSION, # 版本(每次更新上传Pypi需要修改)
      description="Speed up restframework develop",
      long_description=long_description, # 放README.md文件,方便在Pypi页展示
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='restframework utils', # 关键字
      author='helvetica', # 用户名
      author_email='xidianlz@gmail.com', # 邮箱
      url='https://github.com/taizilongxu/douban.fm', # github上的地址,别的地址也可以
      license='MIT', # 遵循的协议
      packages=['rfw_utils', "rfw_utils.management", "rfw_utils.management.commands"], # 发布的包名
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'django',
        'djangorestframework'
      ], # 满足的依赖
)
