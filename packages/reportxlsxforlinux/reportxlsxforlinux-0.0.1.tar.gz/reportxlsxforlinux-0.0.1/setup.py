from setuptools import setup, find_packages
# 确定操作系统

setup(
    name='reportxlsxforlinux',
    version='0.0.1',
    packages=find_packages(),
    package_data={
        'reportxlsxforlinux': ['resources/windows/*.dll','resources/linux/*.dll'],
    },
    include_package_data=True,
    install_requires=[
        'pandas','openpyxl','pythonnet','aspose-cells==24.5.0'
    ],
    description='这是一个操作xlsx的库,只为linux而生',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bailulue',
    author='bailu',
    author_email='yabailu@chinatelecom.cn'
)
