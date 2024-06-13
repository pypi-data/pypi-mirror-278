import unittest
import os
from cypherkit import steganography
from PIL import Image

class TestSteganography(unittest.TestCase):

    def setUp(self):
        self.test_image = 'test_image.png'
        self.output_image = 'encoded_image.png'
        self.message = 'This is a secret message'
        
        # Create a simple test image
        image = Image.new('RGB', (100, 100), color='white')
        image.save(self.test_image)

    def tearDown(self):
        if os.path.exists(self.test_image):
            os.remove(self.test_image)
        if os.path.exists(self.output_image):
            os.remove(self.output_image)

    def test_encode_decode_message(self):
        # Test encoding and decoding a message
        steganography.encode_message(self.test_image, self.message, self.output_image)
        decoded_message = steganography.decode_message(self.output_image)
        self.assertEqual(decoded_message, self.message)

if __name__ == "__main__":
    unittest.main()
