from setuptools import setup

readme = open("./README.md", "r")

setup(
    name='example_package_alexis',
    version='0.0.1',
    description='Esta es la descripción del paquete',
    long_description=readme.read(),
    author='Alexis Barria',
    author_email='alexis.barria.c@outlook.cl',
    classifiers=[],
    license='MIT',
    include_package_data=True
)