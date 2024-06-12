from setuptools import setup, find_packages

# Replace with your library name and version
LIBRARY_NAME = 'echo_alpha'
VERSION = '0.1.0'

setup(
  name=LIBRARY_NAME,
  version=VERSION,
  packages=find_packages(exclude=['tests*']),  # Exclude test directories
  author='Niro',
  author_email='your_email@example.com',
  description='A Python library for (describe your library functionality)',
  install_requires=['pandas','numpy','openai','requests'],
)
