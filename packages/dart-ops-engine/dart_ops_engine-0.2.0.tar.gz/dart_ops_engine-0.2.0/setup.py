from setuptools import setup, find_packages

setup(
    name='dart_ops_engine',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    author='君赏',
    author_email='josercc@163.com',
    description='一个可以被Dart dart_ops_engine执行的Python脚本引擎',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DartOpsHub/dart_ops_engine_python',
)
