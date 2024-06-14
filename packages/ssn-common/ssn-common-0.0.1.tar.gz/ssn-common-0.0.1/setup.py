

from setuptools import setup, find_packages

setup(
    name='ssn-common',
    version = '0.0.1',
    description = 'common utils',
    author='chengdonglin',
    author_email='chengdong2518@163.com',
    requires=['numpy'],  # 定义依赖哪些模块
    packages=['common'], # 需要处理的包目录（包含__init__.py的文件夹）
    exclude_package_data={'':['README.md'],'tests':['*.py']},
    url='https://github.com/chengdonglin/ssn-common'
)