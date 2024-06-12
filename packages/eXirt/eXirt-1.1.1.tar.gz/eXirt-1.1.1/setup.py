from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='eXirt',
      description='Explainable Artificial Intelligence tool base in Item Response Theory.',
      author='José de Sousa Ribeiro Filho',
      author_email='jose.sousa.filho@gmail.com',
      version='1.1.1',
      packages=['pyexirt'],
      license='CC0 1.0 Universal',
      install_requires=['rpy2','pandas','numpy','openml','wget','catsim']
      )

