from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """This function will return the list of requirements"""
    
    requirement_list : List[str] = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                
                # ignore -e . and empty lines
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
                    
    except FileNotFoundError:
        print("requirements.txt file not found.")
        
    return requirement_list

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Ranjith',
    author_email='its.ranjith95@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
    
)

