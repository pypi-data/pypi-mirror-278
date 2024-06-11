import unittest
from unittest.mock import MagicMock
from jrnl2tumblr.tumblr import create_tumblr_client, post_entries_to_tumblr

class TestTumblr(unittest.TestCase):
    def setUp(self):
        self.entries = [
            {"title": "Entry 1", "body": "This is the first entry.", "tags": ["test"]},
            {"title": "Entry 2", "body": "This is the second entry.", "tags": ["test", "second"]},
        ]
        self.client = MagicMock()

    def test_create_tumblr_client(self):
        client = create_tumblr_client('key', 'secret', 'token', 'secret')
        self.assertIsNotNone(client)

    def test_post_entries_to_tumblr(self):
        post_entries_to_tumblr(self.entries, self.client, 'test_blog')
        self.assertEqual(self.client.create_text.call_count, 2)

if __name__ == '__main__':
    unittest.main()
