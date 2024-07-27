import unittest
from app.profanity_checker import detect_toxicity


class TestProfanityChecker(unittest.TestCase):

    def test_profanity(self):
        self.assertTrue(detect_toxicity("This is a bad word!"))  # Example of obscene text
        self.assertFalse(detect_toxicity("This is a good text."))  # Example of normal text


if __name__ == "__main__":
    unittest.main()
