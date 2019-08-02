from codecs import open
from os.path import join, abspath, dirname
from setuptools import setup, find_packages

here = abspath(dirname(__file__))

# Get the long description from the README file
with open(join(here, 'README.rst'), encoding='utf-8') as buff:
    long_description = buff.read()

setup(
    name='date_guesser',
    version='2.1.3',
    description='Extract publication dates from web pages',
    long_description=long_description,
    author='Colin Carroll',
    author_email='ccarroll@mit.edu',
    url='https://github.com/mitmedialab/date_guesser',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['test']),
    install_requires=['arrow>=0.12.0' ,
                      'beautifulsoup4>=4.6.0' ,
                      'lxml>=4.1.1' ,
                      'pytz>=2017.3' ],
    include_package_data=True,
)
