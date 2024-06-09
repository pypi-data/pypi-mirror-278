from setuptools import setup, find_packages

setup(
    name='snake-crypter',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'snake-crypter=snakecrypter.cli:main',
        ],
    },
    author='LNodesL',
    author_email='lnodesl@yahoo.com',
    description='A Python package to encrypt and run programs using XOR encryption',
    license='MIT',
    keywords='encryption decryption XOR c++ cli c crypter',
)
