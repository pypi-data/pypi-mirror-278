#%%

from setuptools import setup, find_packages

setup(
    name='rwend_tools',
    version='1.1',
    packages=['rwend_tools'],
    install_requires=[
        'pyyaml'
    ],
    # Other metadata
    author='Ryan Wendling',
    url='https://github.com/rd-wendling/rwend-tools',
)