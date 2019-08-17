from distutils.core import setup

setup(
  name = 'datascroller',
  packages = ['datascroller'],
  version = '0.9',
  license='MIT',
  description = 'Data scrolling in the terminal',
  author = 'Ben Ogorek',
  author_email = 'baogorek@gmail.com',
  url = 'https://github.com/baogorek/datascroller',
  download_url = 'https://github.com/baogorek/datascroller/archive/v0.9.tar.gz',
  keywords = ['data', 'dataframe', 'viewer'],
  install_requires=[
          'curses',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
