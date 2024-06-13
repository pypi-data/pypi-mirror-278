import unittest
from cypherkit import hashing

class TestHashing(unittest.TestCase):

    def test_generate_verify_hash(self):
        data = "my_data"
        hash_value = hashing.generate_hash(data)
        self.assertTrue(hashing.verify_hash(data, hash_value))

if __name__ == "__main__":
    unittest.main()
