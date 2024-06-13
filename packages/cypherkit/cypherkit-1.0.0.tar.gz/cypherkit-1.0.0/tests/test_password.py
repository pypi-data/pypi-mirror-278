import unittest
from cypherkit import password

class TestPassword(unittest.TestCase):

    def test_hash_verify_password(self):
        pw = "my_secure_password"
        hashed_pw = password.hash_password(pw)
        self.assertTrue(password.verify_password(hashed_pw, pw))

    def test_generate_password(self):
        generated_pw = password.generate_password(16)
        self.assertEqual(len(generated_pw), 16)

if __name__ == "__main__":
    unittest.main()
