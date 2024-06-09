import argparse
from snakecrypter.encryptor import encrypt_file

def main():
    parser = argparse.ArgumentParser(description='Encrypt a C/C++ executable file and generate a self-contained run.py script.')
    parser.add_argument('input_file', type=str, help='Path to the C/C++ executable file')
    parser.add_argument('key', type=str, help='Encryption key')
    args = parser.parse_args()
    
    encrypt_file(args.input_file, args.key)

if __name__ == '__main__':
    main()
