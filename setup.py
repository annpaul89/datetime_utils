from distutils.core import setup

setup(
    name='datetime_utils',
    version='0.1',
    packages=[
        'datetime_utils',
    ],
    url='https://github.com/annpaul89/datetime_utils',
    description='Python functions for common operations on datetime instances',
    install_requires=[
        'pytz>=2016.4',
    ]
)