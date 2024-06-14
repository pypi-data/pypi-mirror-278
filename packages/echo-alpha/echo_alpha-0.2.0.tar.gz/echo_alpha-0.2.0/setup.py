from setuptools import setup, find_packages

# Replace with your library name and version
LIBRARY_NAME = 'echo_alpha'
VERSION = '0.2.0'

setup(
  name=LIBRARY_NAME,
  version=VERSION,
  packages=find_packages(exclude=['tests*','echo_alpha']),  # Exclude test directories
  author='Niro',
  author_email='niro@echo.com',
  description='A Python library for (describe your library functionality)',
  install_requires=['requests','python-dotenv'],
)
