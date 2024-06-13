# CypherKit

CypherKit is a Python library for cryptographic operations, including hashing, password management, file encryption, communication encryption, and steganography.

## Features

- **Password Management:**
  - `hash_password`, `verify_password`, `generate_password`: Functions for hashing, verifying passwords, and generating random passwords.
  
- **File Encryption:**
  - `encrypt_file`, `decrypt_file`: Functions for encrypting and decrypting files using AES encryption.
  
- **Hashing:**
  - `generate_hash`, `verify_hash`: Functions for generating and verifying SHA-256 hashes.
  
- **Communication Encryption:**
  - `encrypt_message`, `decrypt_message`: Functions for encrypting and decrypting messages using AES encryption.
  
- **Steganography:**
  - `encode_message`, `decode_message`: Functions for hiding and retrieving messages within images using LSB (Least Significant Bit) technique.

## Project Structure
```
cypherkit/
├── cypherkit/
│   ├── __init__.py
│   ├── password.py
│   ├── file_crypto.py
│   ├── hashing.py
│   ├── communication.py
│   ├── steganography.py
├── tests/
│   ├── test_password.py
│   ├── test_file_crypto.py
│   ├── test_hashing.py
│   ├── test_communication.py
│   ├── test_steganography.py
├── README.md
├── LICENSE
├── setup.py
```
## Installation

You can install CypherKit using pip. Here's how:

```bash
pip install cypherkit
```
## Usage
**Password Management:**
```
from cypherkit import hash_password, verify_password, generate_password

# Hash and verify a password
hashed_pw = hash_password("my_secure_password")
print(verify_password(hashed_pw, "my_secure_password"))  # True

# Generate a random password
password = generate_password(length=12)
print(password)
```
**File Encryption:**
```
from cypherkit import encrypt_file, decrypt_file

# Encrypt a file
encrypt_file('plaintext.txt', 'password123')

# Decrypt a file
decrypt_file('plaintext.txt.enc', 'password123')

```
**Communication Encryption:**
```
from cypherkit import encrypt_message, decrypt_message
import os

# Generate a random key
key = os.urandom(32)

# Encrypt and decrypt a message
encrypted_msg = encrypt_message("Hello, World!", key)
decrypted_msg = decrypt_message(encrypted_msg, key)
print(decrypted_msg)

```
**Steganography:**
```
from cypherkit import encode_message, decode_message

# Encode a message into an image
encode_message('image.png', 'This is a secret message', 'encoded_image.png')

# Decode a message from an image
decoded_msg = decode_message('encoded_image.png')
print(decoded_msg)

```


## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! If you'd like to contribute to CypherKit, please fork the repository and create a pull request with your changes.