import os
import sys
from tempfile import NamedTemporaryFile
import subprocess

def xor_encrypt(input_bytes, key):
    key_bytes = key.encode()
    output_bytes = bytearray(input_bytes)
    for i in range(len(output_bytes)):
        output_bytes[i] ^= key_bytes[i % len(key_bytes)]
    return bytes(output_bytes)

def generate_run_script(encrypted_data, key):
    from tempfile import NamedTemporaryFile, mkstemp
    import os
    import subprocess

    # Convert encrypted data to hexadecimal for embedding in the Python script
    encrypted_hex = ''.join(format(x, '02x') for x in encrypted_data)

    # Define the content of the Python script that will decrypt and execute the data
    script_content = f"""import os, subprocess
from tempfile import mkstemp

# Key for decryption
key = '{key}'

# Encrypted data in hexadecimal
encrypted_hex = '{encrypted_hex}'

# Convert hex to bytes
encrypted_data = bytes.fromhex(encrypted_hex)

# Decrypt data
decrypted_data = bytearray(encrypted_data)
for i in range(len(decrypted_data)):
    decrypted_data[i] ^= ord(key[i % len(key)])

# Create a new temporary file for the decrypted executable
fd, path = mkstemp(suffix='.out')
os.close(fd)  # Close the file descriptor immediately

# Write the decrypted data to the file
with open(path, 'wb') as f:
    f.write(decrypted_data)
os.chmod(path, 0o755)

# Execute the decrypted file
subprocess.run([path])

# Clean up the temporary file after execution
os.unlink(path)
"""

    # Write the script content to a named temporary Python file
    with NamedTemporaryFile(delete=False, suffix='.py', mode='w') as tmp_file:
        tmp_file.write(script_content)
        os.chmod(tmp_file.name, 0o755)

    # Return the path of the temporary Python script
    return tmp_file.name


def encrypt_file(input_path, key):
    with open(input_path, 'rb') as f:
        input_data = f.read()
    encrypted_data = xor_encrypt(input_data, key)
    run_script_path = generate_run_script(encrypted_data, key)
    print(f'Run script generated at {run_script_path}')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python encryptor.py <input_file> <key>", file=sys.stderr)
        sys.exit(1)
    encrypt_file(sys.argv[1], sys.argv[2])
