from setuptools import setup

setup(name='osy',
      version='0.2.4',
      author='__token__',
      description='description',
      packages=['osy'],
      author_email='skip@mail.ru',
      zip_safe=False,
      include_package_data=True,
      package_data={'osy': ['data/*.csv']},
      install_requires=['setuptools'])
