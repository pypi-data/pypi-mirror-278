from pathlib import Path
from setuptools import setup


setup(
    name='fb2reader',
    version='1.0.2',
    author='Roman Kudryavskyi',
    author_email='devpilgrim@gmail.com',
    packages=['fb2reader'],
    url='https://github.com/devpilgrin/fb2reader',
    license='Apache-2.0 license',
    description='Read data and metadata for fb2 files',
    long_description_content_type='text/markdown',
    long_description=(Path(__file__).parent / "README.md").read_text(),
    keywords=['ebook', 'metadata', 'fb2'],
    classifiers=[
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    install_requires=['bs4']
)