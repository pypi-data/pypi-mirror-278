from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

def requirements():
  a = []
  with open('requirements.txt', 'r') as f:
    a = f.read()
  b = a.split()
  return b

setup(
  name='danila-lib',
  version='2.0.8',
  author='arseniy_zhuck',
  author_email='arseniyzhuck@mail.ru',
  description='This is the module for detecting and classifying text on rama pictures',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Arseniy-Zhuck/danila_lib',
  packages=find_packages(),
  install_requires=requirements(),
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='rama detect machine-learning computer-vision',
  project_urls={
    'GitHub': 'https://github.com/Arseniy-Zhuck/danila_lib'
  },
  python_requires='>=3.6'
)