from setuptools import setup,find_packages

setup(
    name='rtms_sdk',
    version='0.1.14',
    description='plc connect',
    author='Bao Yun',
    author_email='305713412@qq.com',
    packages=find_packages(),
    install_requires=[
        'snap7==0.4',
    ]
)