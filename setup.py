from setuptools import setup, find_packages

setup(
    name="plotter",
    packages=find_packages(),
    install_requires=[
        'click',
        'requests'
    ],
    version='0.0.0',
    entry_points='''
    [console_scripts]
    plotter=plotter:base
    '''
)