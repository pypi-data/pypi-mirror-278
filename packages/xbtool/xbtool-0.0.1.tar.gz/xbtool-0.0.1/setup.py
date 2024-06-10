from setuptools import setup, find_packages
 
setup(
    name='xbtool',
    version='0.0.1',
    packages=find_packages(),
    description='A library of your own tools',
##    long_description=open('README.md').read(),
    # python3，readme文件中文报错
    # long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
##    url='http://github.com/yourusername/my_package',
    author='XiangBing',
    author_email='2677506404@qq.com',
    license='MIT',
    install_requires=[
        # 依赖列表
    ],
    classifiers=[
        # 分类信息
    ]
)
