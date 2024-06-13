import unittest
import os
from cypherkit import file_crypto

class TestFileCrypto(unittest.TestCase):

    def setUp(self):
        self.file_path = 'test_file.txt'
        self.encrypted_path = 'test_file.txt.enc'
        self.password = 'my_secure_password'
        with open(self.file_path, 'w') as f:
            f.write("This is a test file")

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        if os.path.exists(self.encrypted_path):
            os.remove(self.encrypted_path)

    def test_encrypt_decrypt_file(self):
        file_crypto.encrypt_file(self.file_path, self.password)
        self.assertTrue(os.path.exists(self.encrypted_path))

        file_crypto.decrypt_file(self.encrypted_path, self.password)
        with open(self.file_path, 'r') as f:
            data = f.read()
        self.assertEqual(data, "This is a test file")

if __name__ == "__main__":
    unittest.main()
