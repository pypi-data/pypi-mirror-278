from setuptools import setup, find_packages
def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='zubrby',
  version='1.1.4',
  author='aliaksei_ivanko',
  author_email='aleksei.ivanko@gmail.com',
  description='This is the simplest module for quick work with files.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/stncc-bit',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files zubr ',
  project_urls={
    'GitHub': 'https://github.com/stncc-bit'
  },
  python_requires='>=3.6'
)