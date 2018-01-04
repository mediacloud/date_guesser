from codecs import open
from os.path import join, abspath, dirname
from setuptools import setup, find_packages

here = abspath(dirname(__file__))

# Get the long description from the README file
with open(join(here, 'README.rst'), encoding='utf-8') as buff:
    long_description = buff.read()

requirements_file = join(here, 'requirements.txt')

with open(requirements_file) as f:
    install_reqs = f.read().splitlines()

setup(
    name='date_guesser',
    version='0.0.1',
    description='Extract publication dates from web pages',
    long_description=long_description,
    author='Colin Carroll',
    author_email='ccarroll@mit.edu',
    url='https://github.com/ColCarroll/date_guesser',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['test']),
    install_requires=install_reqs,
    include_package_data=True,
)
