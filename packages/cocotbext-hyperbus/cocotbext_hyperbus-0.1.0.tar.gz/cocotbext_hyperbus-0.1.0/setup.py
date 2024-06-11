# setup.py
from setuptools import setup, find_packages

setup(
    name='cocotbext_hyperbus',
    version='0.1.0',
    description='A cocotb extension for HyperBus controllers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/cocotbext_hyperbus',
    packages=find_packages(),
    install_requires=[
        'cocotb',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.8',
)

