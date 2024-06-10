from setuptools import setup
import os

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyoura',
    version='0.1.5',
    description='A Python library for creating command-line spinners',
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    author='Jack',
    author_email='kinginjack@gmail.com',
    packages=['pyoura'],
    install_requires=[],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pyoura=pyoura.__main__:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
