from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='m2metricforge',
  version='0.0.3',
  author='m2syndicate',
  author_email='mtwosyndicate@gmail.com',
  description='Library for generating validation dataset and evaluation metrics',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/HDD-Team/metricforge',
  packages=find_packages(),
  install_requires=[
    'langchain-core',
    'langchain-community',
    'pandas',
    'scikit-learn',
    'pandas',
    'json',
    'requests>=2.25.1'
  ],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent'
  ],
  keywords='metric,validation,generate',
  project_urls={
    'Documentation': 'https://github.com/HDD-Team/metricforge/blob/main/README.MD'
  },
  python_requires='>=3.7'
)
