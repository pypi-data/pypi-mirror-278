from setuptools import setup, find_packages
from setuptools.command.install import install as _install
import subprocess


# Function to read the requirements file
def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()
    

        
setup(
    name='pdf-processor-xyz',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pdf_process=my_pdf_package.pdf_processor:main',
        ],
    },
    install_requires=read_requirements(),

    author='Baha Arfaoui',
    author_email='baha.arfaoui01@gmail.com',
    description='A package to process PDF files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
