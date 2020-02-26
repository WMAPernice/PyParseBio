from distutils.core import setup

VERSION = '0.1'

setup(
  name = 'PyParseBio',
  packages = ['PyParseBio'],
  version = '0.1',
  license='Apache 2.0',
  description = 'Pure-python parralelizable parsing of biological multipoint images',
  author = 'Wolfgang Pernice',
  author_email = 'wolfgang.pernice@gmail.com',
  url = 'https://github.com/WMAPernice/PyParseBio',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
  keywords = ['Biology', 'Microscopy', 'Images', 'Python', 'Parallel'],
  install_requires=[
          'numpy',
          'scikit-image',
		  'nd2reader>=3.2.3'
		  'tqdm',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      	
    'Intended Audience :: Science/Research',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache 2.0 License',  		
    'Programming Language :: Python :: 3.6',
  ],
)