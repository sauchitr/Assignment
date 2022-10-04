import unittest
import os
from Convert import Convert


class TestConvert(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("setupclass")

    @classmethod
    def tearDownClass(cls):
        print("teardownclass")

    def setUp(self):
        self.file1 = "DLTINS_20210117_01OF01.xml"
        self.file2 = "output.csv"

    def tearDown(self):
        del self.file1
        del self.file2

    def test_file_extracted(self):
        if Convert.extract_file(Convert("1.zip")):
            self.assertTrue(self.file1, msg="File is created")

    def test_file_created(self):
        if Convert.convert_file(Convert("DLTINS_20210117_01OF01.xml")):
            self.assertTrue(self.file2, msg="File is created")


if __name__ == "__main__":
    unittest.main()
