from setuptools import setup, find_packages

setup(
    name = 'check_if_is_production',
    packages = ['check_if_is_production'],   
    version = '0.0.1',
    description = 'Check if an Odoo conneciton is running in production or not',
    author='Mateo De León',
    author_email="mdeleon@proyectasoft.com",
    license="GPLv3",
    url="https://github.com/mateo-de-leonn/check_production_running",
    classifiers = ["Programming Language :: Python :: 3",\
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",\
        "Operating System :: OS Independent"],
    python_requires='>=3.9',
    )