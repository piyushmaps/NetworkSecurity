'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''
#find_packages will go through the folder and where __init__ file will be there it will make package of that folder

from setuptools import setup, find_packages
from typing import List


requirement_lst: List[str]=[]
def get_requirements()-> List[str]:
    """
    This function will return list of requirements"""

    try:
        with open('requirements.txt','r') as file:
            #Read line from the file
            lines=file.readlines()
            ##Process each line
            for line in lines:
                requirement=line.strip()
                ##ignore the empty line and -e. rquirement first time means if requirement exist and not equal to "-e"
                if requirement and requirement != "-e .":
                    requirement_lst.append(requirement)
    except  FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst

print(get_requirements())
#setting up the metada

setup(
    name="NetworkSecurity",
    version='0.0.1',
    author="Piyush",
    author_email="piyushthakur3613@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()

)

#-e. is refering to setup.py file when we install the dependencies using pip install -r requirements.txt
#so all the packages and meta data can be intiated
