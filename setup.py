from setuptools import setup

setup(
    name='ConsumeEventhub',
    version='1.0',
    py_modules=['consumer'],
    install_requires=['Click', 'azure-eventhub'],
    entry_points='''
    [console_scripts]
    eventhub-consume=consumer:cli
    '''
)