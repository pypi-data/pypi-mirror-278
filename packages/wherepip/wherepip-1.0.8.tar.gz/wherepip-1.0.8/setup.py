from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wherepip',
    version='1.0.8',
    description='高效python库管理工具,功能有搜索、安装、卸载、获取库所在目录（python学霸公众号）',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Python学霸',
    author_email='python@xueba.com',
    py_modules=['wherepip'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'whereis=wherepip:whereis',
            'fuck=wherepip:fuck',
            'befuck=wherepip:befuck',
            'so=wherepip:so',
            'all=wherepip:all'
        ]
    }
)