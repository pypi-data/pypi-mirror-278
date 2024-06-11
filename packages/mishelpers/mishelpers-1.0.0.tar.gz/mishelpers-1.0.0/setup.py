from setuptools import setup, find_packages

print(f'Packages: {find_packages}')

setup(
  name='mishelpers',
  version='1.0.0',
  description='Un paquete con helpers',
  long_description='## Un *paquete* con **helpers**',
  long_description_content_type='text/markdown',
  author='Ángel Villalba',
  author_email='angelisco92@gmail.com',
  packages=find_packages()
)