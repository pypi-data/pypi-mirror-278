from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='polip',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vladyslav',
    author_email='vladdikiy17@gmai.com',
    url='https://github.com/dykyivladk1/polip',
    include_package_data=True,
)
