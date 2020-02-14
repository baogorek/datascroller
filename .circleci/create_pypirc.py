#!/usr/env/python
import sys

def main(argv):
  
    pypirc_text = """
    [distutils]
    index-servers=
        pypi
        testpypi
    
    [pypi]
    username: {user} 
    password: {passwd} 
    
    [testpypi]
    repository: https://test.pypi.org/legacy/
    username: {user} 
    password: {passwd}
    """
    return pypirc_text.format(user=argv[1], passwd=argv[2])

if __name__ == '__main__':
    print(main(sys.argv))
