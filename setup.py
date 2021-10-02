from setuptools import setup
  
description = "I have yet to write this"
  
# specify requirements of your package here
REQUIREMENTS = ['pygame']
  
# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    ]
  
# calling the setup function 
setup(name='pyLdtk',
      version='0.0.3',
      description='Just some quick and simple groundwork for working with ldtk in python. VERY EARLY STAGES!',
      long_description=description,
      url='https://github.com/LGgameLAB/pyLdtk',
      author='Luke Gonsalves',
      author_email='lukegonsalves07@gmail.com',
      license='MIT',
      packages=['pyLdtk'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='ldtk LDTK python pygame py Tiled tile tileset game'
      )