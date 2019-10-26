from distutils.core import setup

LONG_DESCRIPTION = """
datascroller - data scrolling in the terminal!

Welcome to the datascroller project! While IDEs and notebooks are excellent
or interactive data exploration, there will always be some of us who prefer
to stay in the terminal. For exploring Pandas data frames, that meant
painstakingly tedius use of .iloc, until now...
"""

setup(
  name='datascroller',
  packages=['datascroller'],
  version='1.1.0',
  license='MIT',
  description='Data scrolling in the terminal',
  long_description=LONG_DESCRIPTION,
  long_description_content_type='text/markdown',
  author='Ben Ogorek',
  author_email='baogorek@gmail.com',
  url='https://github.com/baogorek/datascroller',
  download_url='https://github.com/baogorek/datascroller/archive/v1.1.0.tar.gz',
  keywords = ['data', 'dataframe', 'viewer'],
  install_requires=[
          'pandas',
          'windows-curses ; platform_system=="Windows"',
      ],
  scripts=['bin/scroll'],
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
