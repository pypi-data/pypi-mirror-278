from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line and not line.startswith('#')]

setup(
   name='bollm',
   version='0.0.6',
   author='Steven Brooks',
   author_email='steven.brooks@boehringer.com',
   description='Framework for building LLM-based apps in Boehringer Ingelheim',
   long_description=open('README').read(),
   long_description_content_type='text/markdown',
   url='https://bitbucket.biscrum.com/projects/MAGIC/repos/billm/browse',
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
   ],
   packages=find_packages(where='.'),
   package_dir={'': '.'},
   python_requires='>=3.9',
   install_requires=parse_requirements('requirements.txt')
)