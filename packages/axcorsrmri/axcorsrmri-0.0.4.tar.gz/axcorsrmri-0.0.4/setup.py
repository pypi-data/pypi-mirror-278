from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='axcorsrmri',
    version='0.0.4',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Technion Computational MRI Lab',
    author_email='tcml.bme@gmail.com',
    url='https://github.com/TechnionComputationalMRILab/AxCorSRMRI',
    packages=find_packages(),
    install_requires=requirements,
)
