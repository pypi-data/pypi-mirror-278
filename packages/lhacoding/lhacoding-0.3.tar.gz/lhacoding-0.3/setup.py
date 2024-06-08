from setuptools import setup, find_packages

setup(
    name='lhacoding',
    version='0.3',
    description='Python functions for controlling Arduino devices',
    author='LEE HYUN A',
    author_email='lha110@naver.com',
    packages=find_packages(),
    install_requires=['pyserial'],
)
