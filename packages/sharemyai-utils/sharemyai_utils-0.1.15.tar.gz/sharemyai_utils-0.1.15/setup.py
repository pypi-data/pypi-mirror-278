from setuptools import setup, find_packages                                     
import codecs                                                                   
import os                                                                       
import re      

def find_version(*file_paths):                                                  
    # Open in Latin-1 so that we avoid encoding errors.                         
    # Use codecs.open for Python 2 compatibility                                
    here = os.path.abspath(os.path.dirname(__file__))                           
    with codecs.open(os.path.join(here, *file_paths), 'r', 'latin1') as f:      
        version_file = f.read()                                                 

    # The version line must have the form                                          
    # __version__ = 'ver'                                                       
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",            
                              version_file, re.M)                               
    if version_match:                                                           
        return version_match.group(1)                                           
    raise RuntimeError("Unable to find version string.")                                                                 

long_description = """
Reusable utilities for ShareMyAI. For more information, visit [ShareMyAI](https://sharemy.ai).
"""

setup(                                                                          
    name="sharemyai_utils",                                                             
    version=find_version('sharemyai_utils', '__init__.py'),                             
    description="Reusable utils for sharemyai plugins",                    
    long_description=long_description,                                          
    url='http://github.com/catswithkeyboards',                                   
    author='Cats with Keyboards',                                                     
    author_email='tech@catswithkeyboards.com',                                     
    license='',                                    
    classifiers=[                                                               
        'Development Status :: 3 - Alpha',       
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: Free for non-commercial use'
    ],                                                                          
    keywords='sharemyai utils',                                                  
    packages=find_packages(exclude=["tests*", "*.env", "scripts"]),                                 
    install_requires=[   
        "click",
        "psutil==5.9.8",
        "pillow",
        "flask==3.0.2",
        "flask_cors==4.0.0",
        "flask-sock==0.7.0",
        "httptools==0.6.1",
        "opencv-python==4.9.0.80",
        "requests",
        "python-dotenv",
        "websockets"                                                 
    ],   
    entry_points={
        "console_scripts": [
            "sharemyai = cli:cli"
        ]
    },                                                                       
)      