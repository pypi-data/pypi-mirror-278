from setuptools import setup, find_packages


setup(
    name="nest-sw",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.1',
        'pandas>=1.5.3',
        'nibabel>=5.0.0',
        'nilearn>=0.10.3',
        'matplotlib>=3.6.3',
        'hcp_utils>=0.1.0',
        'scikit-learn>=1.2.1'
    ],
    # Metadata
    author="Sarah Weinsten",
    author_email="sarah.m.weinsten@temple.edu",
    description="The Python implementation of the NEST method.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/smweinst/NEST/tree/main/Python",  
)