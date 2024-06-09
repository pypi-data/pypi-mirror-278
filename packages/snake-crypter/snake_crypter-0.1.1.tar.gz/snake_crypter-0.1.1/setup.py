from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='snake-crypter',
    version='0.1.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'snake-crypter=snakecrypter.cli:main',
        ],
    },
    author='LNodesL',
    author_email='lnodesl@yahoo.com',
    description='A Python package to encrypt and run programs using XOR encryption',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    keywords='encryption decryption XOR c++ cli c crypter',
)
