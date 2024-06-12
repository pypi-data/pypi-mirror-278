#%%

from setuptools import setup, find_packages

setup(
    name='rwend_tools',
    version='1.2',
    packages=['rwend_tools'],
    install_requires=[
        'pyyaml',
        'googlemaps'
    ],
    # Other metadata
    author='Ryan Wendling',
    url='https://github.com/rd-wendling/rwend-tools',
)