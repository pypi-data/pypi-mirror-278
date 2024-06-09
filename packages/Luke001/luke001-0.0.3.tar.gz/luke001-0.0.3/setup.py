from setuptools import setup, find_packages


def readme():
  with open('ReadME.md', 'r') as f:
    return f.read()


setup(
  name='Luke001',
  version='0.0.3',
  author='undefined',
  author_email='c3pe0@gmail.com',
  description='May the force be with you',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='May the force be with you ',
  project_urls={
  },
  python_requires='>=3.6'
)