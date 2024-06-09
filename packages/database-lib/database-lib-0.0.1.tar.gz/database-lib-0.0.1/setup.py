from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='database-lib',
  version='0.0.1',
  description='A basic sqlite3 editing library',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Theodor Billek',
  author_email='HilbertLooked@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='database',
  packages={'database_lib': 'src'},  
  install_requires=[''] 
)
