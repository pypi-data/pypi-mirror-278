from setuptools import setup, find_packages

setup(
    name='filchatter',
    version='2.0',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'filchatter=filchatter:main'
        ]
    },
)