from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='mazefulltasker',
  version='0.0.1',
  author='mazefull',
  author_email='mazefull@gmail.com',
  description='Simply task tracker for python.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://t.me/mazefull',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/mazefull/'
  },
  python_requires='>=3.10'
)
