import unittest

from .storage_composite import StorageComposite


class TestStorageComposite(unittest.TestCase):
    def setUp(self):
        self.storage = StorageComposite()


if __name__ == "__main__":
    unittest.main()
