import shutil
import tempfile
import os
import requests
import imghdr

from os import path
from unittest import TestCase
from vivotool.utils.file_utils import Utils


class TestFileUtils(TestCase):

    def setUp(self):
        self.utils = Utils()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        self.utils = None
        shutil.rmtree(self.test_dir)

    def test_save_photo_file(self):
        testfile = path.join(self.test_dir, 'test.png')
        content = requests.get(
            "https://www.iconfinder.com/icons/216359/download/png/128")

        self.utils.save_photo_file(content, testfile)
        output = imghdr.what(testfile)
        self.assertEqual(output, "png")

    def test_read_file(self):
        testfile = path.join(self.test_dir, 'test.txt')

        with open(testfile, "w") as f:
            f.write("some content")

        output = self.utils.read_file(testfile)
        self.assertEqual(output, "some content")

    def test_save_xml_file(self):
        testfile = path.join(self.test_dir, 'test.xml')
        content = "<xml>test</xml>"

        self.utils.save_xml_file(content, testfile)

        with open(testfile, 'r') as file:
            output = file.read()
        self.assertEqual(output, content)

    def test_listfiles(self):
        xmlfile = path.join(self.test_dir, 'test.xml')
        txtfile = path.join(self.test_dir, 'test.txt')

        with open(xmlfile, 'w') as f:
            f.write("some content")

        with open(txtfile, 'w') as f:
            f.write("some content")

        expected = ['test.xml']
        output = self.utils.listfiles(self.test_dir, ".xml")
        self.assertEqual(output, expected)

    def test_listdeletefiles(self):
        deletefile = path.join(self.test_dir, 'deletetest.xml')
        txtfile = path.join(self.test_dir, 'test.txt')

        with open(deletefile, 'w') as f:
            f.write("some content")

        with open(txtfile, 'w') as f:
            f.write("some content")

        expected = ['deletetest.xml']
        output = self.utils.listdeletefiles(self.test_dir, "delete")
        self.assertEqual(output, expected)
