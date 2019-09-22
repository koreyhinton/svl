import setuptools
#from distutils.core import setup

setuptools.setup(
    name='svllib',
    version='0.1dev',
    author='Korey Hinton',
    author_email='korey.hinton@mail.com',
    packages=setuptools.find_packages(), #['svl'],
    license='LGPLv3',
    long_description=open('README.md').read(),
    url='https://github.com/koreyhinton/svl',
    python_requires='>=3.7'
)
