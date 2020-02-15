from setuptools import setup

LONG_DESCRIPTION = """
Welcome to the datascroller project! While IDEs and notebooks are excellent
for interactive data exploration, there will always be some of us who prefer
to stay in the terminal. For exploring Pandas data frames, that meant
painstakingly tedius use of `.iloc`, until now...

For more info, please see our github page: github.com/baogorek/datascroller
"""

setup(
    name='datascroller',
    packages=['datascroller'],
    version='1.3.1',
    license='MIT',
    description='Data scrolling in the terminal',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Ben Ogorek, John C. Merfeld, Kevin Merfeld',
    author_email='baogorek@gmail.com, john.merfeld@gmail.com, kevinjmerfeld@gmail.com',
    url='https://github.com/baogorek/datascroller',
    keywords=['data', 'dataframe', 'viewer'],
    include_package_data=True,
    install_requires=[
        'pandas',
        'windows-curses ; platform_system=="Windows"',
        'pandasql'
    ],
    extras_require={
        'testing': ['pytest'],
        'linting': ['flake8'],
    },
    entry_points={
        'console_scripts': [
            'scroll_demo=datascroller.command_line:run_demo',
            'scroll=datascroller.command_line:run_scroll',
            'getkey=datascroller.command_line:run_getkey'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
