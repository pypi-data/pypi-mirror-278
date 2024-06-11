from setuptools import setup, find_packages
# 确定操作系统

setup(
    name='reportXlsx',
    version='0.4.0',
    packages=find_packages(),
    package_data={
        'reportXlsx': ['resources/windows/*.dll','resources/linux/*.dll'],
    },
    include_package_data=True,
    install_requires=[
        'pandas','openpyxl','pythonnet','xlwings'
    ],
    description='这是一个操作xlsx的库,兼容windows和linux',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bailulue',
    author='bailu',
    author_email='yabailu@chinatelecom.cn'
)
