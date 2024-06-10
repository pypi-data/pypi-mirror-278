# setup.py

from setuptools import setup

setup(
    name='pyoura',
    version='0.1.1',
    description='A Python library for creating command-line spinners',
    author='jack',
    author_email='kinginjack@gmail.com',
    packages=['pyoura'],
    install_requires=[
        'colorama',
        'termcolor'
    ],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pyoura=pyoura.__main__:main'
        ]
    }
)

