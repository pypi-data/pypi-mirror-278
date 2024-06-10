# setup.py
from setuptools import setup, find_packages

PACKAGE_NAME = 'ambientctl'
VERSION = '0.2.5'

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'tqdm==4.66.4',
        'pydantic_settings==2.3.1',
    ],
    entry_points={
        'console_scripts': [
            'ambientctl=ambientctl.main:main',
        ],
    },
    author='ambient',
    author_email='jose@ambientlabscomputing.com'
)
