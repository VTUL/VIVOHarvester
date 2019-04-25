import requests
import requests_mock
import tempfile
import os

from os import path
from unittest import TestCase
from vivotool.harvester.elements import Elements
from vivotool.utils.file_utils import Utils
from datetime import datetime, timedelta
from unittest import mock


class TestElements(TestCase):

    def setUp(self):
        self.elements = Elements()
        self.utils = Utils()
        self.test_dir = tempfile.mkdtemp()
        os.makedirs(self.test_dir + "/fullImages/")
        os.makedirs(self.test_dir + "/thumbnails/")

    def tearDown(self):
        self.elements = None

    @requests_mock.mock()
    def test_request_elements(self, m):
        m.get('http://foo.com/photo', text='photo')
        m.get('http://foo.com/user/1003', text='<feed>test</feed>')
        output = self.elements.elements_request(
            'http://foo.com/photo', "", "photo")
        self.assertEqual(output.text, "photo")

        output = self.elements.elements_request("http://foo.com/user/1003", "")
        self.assertEqual(output.decode("utf-8"), "<feed>test</feed>\n")

    def test_get_next_URL(self):

        output = self.elements.get_next_URL("")

        # check empty string
        self.assertEqual(output, "")

        test_xml_content = """<feed xmlns="http://www.w3.org/2005/Atom" xmlns:api="testapi">
                              <api:pagination results-count="9429" items-per-page="25">
                                <api:page position="this" href="https://test.com"/>
                                <api:page position="next" href="https://test.com?after-id=2784"/>
                              </api:pagination>
                            </feed>
                            """

        output = self.elements.get_next_URL(test_xml_content)
        expected = "https://test.com?after-id=2784"
        self.assertEqual(output, expected)

        # test if there is no next URL
        test_xml_content = """<feed xmlns="http://www.w3.org/2005/Atom" xmlns:api="testapi">
                              <api:pagination results-count="9429" items-per-page="25">
                                <api:page position="this" href="https://test.com"/>
                              </api:pagination>
                            </feed>
                            """

        output = self.elements.get_next_URL(test_xml_content)
        expected = ""
        self.assertEqual(output, expected)

        test_xml_content = """<feed xmlns="http://www.w3.org/2005/Atom" xmlns:api="testapi">
                            </feed>
                            """
        output = self.elements.get_next_URL(test_xml_content)
        expected = ""
        self.assertEqual(output, expected)

    def mock_queryurl(elements_endpoint, query_type, params, *day):
        return "http://foo.com/" + query_type + "/" + params

    def mock_elements_request(elementsurl, headers, *category):
        class MockResponse:
            def __init__(self, data, status_code):
                self.data = data
                self.status_code = status_code

        if category and category[0] == "photo":
            return MockResponse("<feed>test</feed>\n", 200)
        else:
            return "<feed>test</feed>\n"

    def mock_save_photo_file(content, filename):
        content = "<feed>test</feed>\n"
        with open(filename, "w") as file:
            file.write(content)

    @mock.patch(
        'vivotool.harvester.elements.Elements.createElementsQueryURL',
        side_effect=mock_queryurl)
    @mock.patch(
        'vivotool.harvester.elements.Elements.elements_request',
        side_effect=mock_elements_request)
    @mock.patch(
        'vivotool.utils.file_utils.Utils.save_photo_file',
        side_effect=mock_save_photo_file)
    def test_harvest_elements_xml(self, m1, m2, m3):

        # test query_type == "photo"
        self.elements.harvest_elements_xml(
            'http://foo.com/', "", "photo", "1003", self.test_dir + "/")

        imagefile1 = path.join(self.test_dir, 'fullImages/1003.jpeg')
        imagefile2 = path.join(self.test_dir, 'thumbnails/1003.jpeg')
        output = self.utils.read_file(imagefile1)
        self.assertEqual(output, "<feed>test</feed>\n")
        output = self.utils.read_file(imagefile2)
        self.assertEqual(output, "<feed>test</feed>\n")

        # test query_type == "users"
        testfile = path.join(self.test_dir, 'testuser.xml')
        self.elements.harvest_elements_xml(
            'http://foo.com/', "", "users", "1003", testfile)
        output = self.utils.read_file(testfile)
        self.assertEqual(output, "<feed>test</feed>\n")

        # test query_type == "publications" with day
        testfile = path.join(self.test_dir, 'testpublications.xml')
        self.elements.harvest_elements_xml(
            'http://foo.com/', "", "publications", "9003", testfile, 10)
        output = self.utils.read_file(testfile)
        self.assertEqual(output, "<feed>test</feed>\n")

        # test query_type = "user"
        testfile = path.join(self.test_dir, 'testsingleuser.xml')
        self.elements.harvest_elements_xml(
            'http://foo.com/', "", "user", "1003", testfile)
        output = self.utils.read_file(testfile)
        self.assertEqual(output, "<feed>test</feed>\n")

    def test_createElementsQueryURL(self):

        elements_endpoint = "http://foo.com"

        # check user queryurl
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "user", 1033)
        self.assertEqual(output, elements_endpoint + "users/1033")

        # check users and day
        harvest_time = self.elements.last_modified_date(5)[:10]
        expected = str(datetime.now() - timedelta(days=5))[:10]
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "users", 25, harvest_time)
        self.assertEqual(
            output,
            elements_endpoint +
            "users?detail=full&per-page=25&modified-since=" +
            expected)

        # check users queryurl
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "users", 25)
        self.assertEqual(
            output,
            elements_endpoint +
            "users?detail=full&per-page=25")

        # check publications and day
        harvest_time = self.elements.last_modified_date(5)[:10]
        expected = str(datetime.now() - timedelta(days=5))[:10]
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "publications", 1033, harvest_time)
        self.assertEqual(
            output,
            elements_endpoint +
            "users/1033/publications?detail=full&per-page=25&modified-since=" +
            expected)

        # check publications
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "publications", 1033)
        self.assertEqual(output, elements_endpoint +
                         "users/1033/publications?detail=full&per-page=25")

        # check publication
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "publication", 1033)
        self.assertEqual(output, elements_endpoint + "publications/1033")

        # check relationship
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "relationship", 1033)
        self.assertEqual(output, elements_endpoint + "relationships/1033")

        # check pubrelationships and day
        harvest_time = self.elements.last_modified_date(5)[:10]
        expected = str(datetime.now() - timedelta(days=5))[:10]
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "pubrelationships", 1033, harvest_time)
        self.assertEqual(
            output,
            elements_endpoint +
            "publications/1033/relationships?detail=full&per-page=25&modified-since=" +
            expected)

        # check pubrelationships
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "pubrelationships", 1033)
        self.assertEqual(
            output,
            elements_endpoint +
            "publications/1033/relationships?detail=full&per-page=25")

        # check photo
        output = self.elements.createElementsQueryURL(
            elements_endpoint, "photo", 1033)
        self.assertEqual(output, elements_endpoint + "users/1033/photo")

        # check invalidated input
        self.assertRaises(
            ValueError,
            lambda: self.elements.createElementsQueryURL(
                elements_endpoint, "xyz", 1033))

    def test_last_modified_date(self):

        day = 1
        output = self.elements.last_modified_date(day)[:10]
        expected = str(datetime.now() - timedelta(days=day))[:10]

        self.assertEqual(output, expected)

        day = "string"
        self.assertRaises(
            ValueError,
            lambda: self.elements.last_modified_date(day)[
                :1])

        day = "1"
        self.assertRaises(
            TypeError,
            lambda: self.elements.last_modified_date(day)[
                :1])

        day = -1
        output = self.elements.last_modified_date(day)[:10]
        expected = ""

        self.assertEqual(output, expected)
