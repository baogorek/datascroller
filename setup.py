from distutils.core import setup

with open('README.md') as f:
        long_description = f.read()

setup(
  name='datascroller',
  packages=['datascroller'],
  version='0.9.2',
  license='MIT',
  description='Data scrolling in the terminal',
  long_description=long_description,
  #long_description_content_type='text/markdown',
  #TODO(baogorek) undo workaround from https://github.com/bloomberg/powerfulseal/pull/159/files
  author='Ben Ogorek',
  author_email='baogorek@gmail.com',
  url='https://github.com/baogorek/datascroller',
  download_url='https://github.com/baogorek/datascroller/archive/v0.9.2.tar.gz',
  keywords = ['data', 'dataframe', 'viewer'],
  install_requires=[
          'pandas',
          'windows-curses ; platform_system=="Windows"',
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
