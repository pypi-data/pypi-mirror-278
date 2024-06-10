from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name='mateoperaciones',
    packages=find_packages(include=['mateoperaciones']),
    version='0.1.0',
    description="libreria de operaciones básicas",
    long_description=description,
    long_description_content_type="text/markdown",
    author='Alexis Ruales',
    license='MIT',
    install_requires=[],
    python_requires=">=3.10.12"
)