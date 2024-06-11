import unittest
from jrnl2tumblr.importer import read_jrnl_file
import os
import json

class TestImporter(unittest.TestCase):
    def setUp(self):
        # Crea un archivo JSON temporal para las pruebas
        self.test_jrnl_file = 'test_jrnl.json'
        self.test_data = [
            {"title": "Entry 1", "body": "This is the first entry.", "tags": ["test"]},
            {"title": "Entry 2", "body": "This is the second entry.", "tags": ["test", "second"]},
        ]
        with open(self.test_jrnl_file, 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        # Elimina el archivo JSON temporal después de las pruebas
        if os.path.exists(self.test_jrnl_file):
            os.remove(self.test_jrnl_file)

    def test_read_jrnl_file(self):
        entries = read_jrnl_file(self.test_jrnl_file)
        self.assertEqual(entries, self.test_data)

if __name__ == '__main__':
    unittest.main()
