import unittest

from .ftp import FtpServer


class TestFtpServer(unittest.TestCase):
    def setUp(self):
        self.ftp = FtpServer("", "", "")


if __name__ == "__main__":
    unittest.main()
