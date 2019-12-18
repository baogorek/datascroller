from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='datascroller',
    packages=['datascroller'],
    version='1.2.0',
    license='MIT',
    description='Data scrolling in the terminal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ben Ogorek',
    author_email='baogorek@gmail.com',
    url='https://github.com/baogorek/datascroller',
    download_url='https://github.com/baogorek/datascroller/archive/v1.1.0.tar.gz',
    keywords=['data', 'dataframe', 'viewer'],
    include_package_data=True,
    install_requires=[
        'pandas',
        'windows-curses ; platform_system=="Windows"',
    ],
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
