from unittest import TestCase
from vivotool.harvester.elements import Elements
from datetime import datetime, timedelta

class TestElements(TestCase):

    def setUp(self):
        self.elements = Elements()

    def tearDown(self):
        self.elements = None


    def test_request_elements(self):
        pass


    def test_get_next_URL(self):
        pass


    def test_last_modified_date(self):

        day = 1
        output = self.elements.last_modified_date(day)[:10]
        expected = str(datetime.now() - timedelta(days=day))[:10]

        self.assertEqual(output, expected)

        day = "string"
        self.assertRaises(ValueError, lambda: self.elements.last_modified_date(day)[:1])

        day = "1"
        self.assertRaises(TypeError, lambda: self.elements.last_modified_date(day)[:1])

        day = -1
        output = self.elements.last_modified_date(day)[:10]
        expected = ""

        self.assertEqual(output, expected)