import os

from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='mapfw',
      version='0.7.0',
      description='API client for mapfw challenges',
      url='https://github.com/noahiscool13/mapfw-client',
      author='Noah Jadoenathmisier',
      author_email='n.j.m.jadoenathmisier@student.tudelft.nl',
      license='MIT',
      packages=['mapfw'],
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      zip_safe=False,
      install_requires=[
          'requests',
          'func_timeout',
          'tqdm',
          'pathos'
      ],
      )
