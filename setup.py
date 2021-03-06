from setuptools import setup

setup(
   name='udapi_agldt',
   version='0.1',
   description='A collection of blocks for the Udapi Python framework, created to provide support for the AGLDT treebanks',
   author='Francesco Mambrini',
   author_email='',
   packages=['udapi_agldt', 'udapi_agldt.read', 'udapi_agldt.util', 'udapi_agldt.write', 'udapi_agldt.query'],
   install_requires=['udapi', 'lxml']
)
