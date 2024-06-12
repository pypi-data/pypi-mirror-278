from setuptools import setup, find_packages
  
# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()
  

# some more details
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: MacOS X',
    'Framework :: IDLE',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.11',
    'Topic :: Scientific/Engineering :: Bio-Informatics'
    'Topic :: Scientific/Engineering :: Information Analysis'
    ]
  
# calling the setup function 
setup(name='HIV_Isoform_Checker',
      version='1.1.0',
      description='Filters .gtf file of suspected HIV isoforms and confirms the isoform identities.',
      long_description=long_description,
      url='https://github.com/JessicaA2019/HIV_Isoform_Checker',
      author='Jessica Lauren ALbert',
      author_email='jessica.albert2001@gmail.com',
      license='MIT',
      packages = find_packages(),
      entry_points = {'console_scripts': ['HIV_Isoform_Checker = HIV_Isoform_Checker.__main__:main']},
      classifiers=CLASSIFIERS,
      keywords='HIV isoforms gtf_file CDS_region ONTsequencing',
      include_package_data = True
      )
