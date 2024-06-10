# setup.py

from setuptools import setup, find_packages

setup(
    name="seachad_libraries",
    version="0.0.1",
    author="jovenluke",
    author_email="fernando.garcia.varela@seachad.com",
    description="Una libreria para escribir en el terminal con colorines, y mas cosas...",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/tu_usuario/mi_libreria",
    packages=find_packages(),
    install_requires=[
        # Aquí van las dependencias de tu paquete, por ejemplo:
        # 'numpy>=1.18.1',
        # 'pandas>=1.0.3',
        'colorama'
    ],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
