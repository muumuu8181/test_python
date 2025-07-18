import unittest
from hello_0718 import hello_0718

class TestHello0718(unittest.TestCase):
    def test_hello_0718(self):
        result = hello_0718()
        self.assertEqual(result, "hello 0718")
        
    def test_hello_0718_output(self):
        # Test that the function returns the expected string
        expected = "hello 0718"
        actual = hello_0718()
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()