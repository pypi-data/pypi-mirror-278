# Snake Crypter

Snake Crypter is a Python package that provides tools to encrypt and decrypt C/C++ executable files, then run them securely. This package is designed to facilitate secure distribution and execution of compiled code.

## Installation

To install Snake Crypter, run the following command in your terminal:

```bash
pip install snake-crypter
```

## Usage

To encrypt and decrypt a C/C++ executable file, use the following commands:

### Encrypting an Executable

```bash
snake-crypter your_executable_file your_key
```

This will generate a `run.py` script that can be used to decrypt and execute the encrypted file from Python.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
