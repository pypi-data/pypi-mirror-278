from setuptools import setup, find_packages

setup(
    name='tnsaai',
    version='0.1.0',
    author='TNSA Artifical Intelligence',
    author_email='thishyakethabimalla@gmail.com',
    description='A transformer-based architecture implemented in PyTorch.',
    packages=find_packages(),
    install_requires=[
        'torch>=1.7.0',
        'tensorflow>=2.4.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
