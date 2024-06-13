from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as file:
        return file.read()

setup(
  name='mailSenderLib',
  version='0.0.1',
  author='BorshCode',
  author_email='rechkinnm@yandex.ru',
  description='Эта библиотека позволит Вам легко обновлять эл. почту.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/borshcode/mailSenderLib.git',
  packages=find_packages(),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='mail sender ',
  project_urls={
    'GitHub': 'https://github.com/borshcode/mailSenderLib'
  },
  python_requires='>=3.6'
)