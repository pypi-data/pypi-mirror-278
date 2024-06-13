import unittest
import os
from cypherkit import communication

class TestCommunication(unittest.TestCase):

    def test_encrypt_decrypt_message(self):
        key = os.urandom(32)
        message = "Hello, World!"
        encrypted_message = communication.encrypt_message(message, key)
        decrypted_message = communication.decrypt_message(encrypted_message, key)
        self.assertEqual(message, decrypted_message)

if __name__ == "__main__":
    unittest.main()
