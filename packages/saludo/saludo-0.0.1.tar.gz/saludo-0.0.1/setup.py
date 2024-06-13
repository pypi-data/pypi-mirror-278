from setuptools import setup

readme = open("./README.md", "r")

setup(
    name='saludo',
    packages=['saludo'],
    version='0.0.1',
    description='Esta es la descripción del paquete',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Alexis Barria',
    author_email='alexis.barria.c@outlook.cl',
    classifiers=[],
    license='MIT',
    include_package_data=True
)

