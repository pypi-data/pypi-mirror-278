from setuptools import setup, find_packages

setup(
    name='hdicoding',
    version='0.2',
    description='Python functions for controlling Arduino devices',
    author='dain0113',
    author_email='hdi5709@naver.com',
    packages=find_packages(),
    install_requires=['pyserial'],
)
