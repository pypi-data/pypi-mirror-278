#%%

from setuptools import setup, find_packages

setup(
    name='rwend_tools',
    version='1.3',
    packages=['rwend_tools'],
    install_requires=[
        'pyyaml',
        'googlemaps',
        'google-cloud-secret-manager'
    ],
    # Other metadata
    author='Ryan Wendling',
    url='https://github.com/rd-wendling/rwend-tools',
)