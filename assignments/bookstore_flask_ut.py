import unittest
import os
import json
import mongomock
import bookapi
import pprint

from app import app
import apymongodb

TEST_DB = 'test_database'


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        """
        Set up a temp database before each test. since this is not end to
        end test use mongomock to create a testdb. This DB will have the same
        schema as that of the original db.
        """
        app.testing = True
        pass

    def tearDown(self):
        """using mongomock for the ut test. Hence no clean up is needed """
        pass

    def test_index(self):
        """initial test. ensure flask was set up correctly"""
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_get_book(self):
        """
        Test the books api
        """
        tester = app.test_client(self)
        response = tester.get('/getbook', content_type='application/json')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)
        pass

    def test_get_book_isbn(self):
        """
        Test the book isbn api
        """
        tester = app.test_client(self)
        response = tester.get('/getbook/123', content_type='application/json')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)

        tester = app.test_client(self)
        response = tester.get('/getbook/1491979909', content_type='application/json')
        print(response.get_json())
        self.assertEqual(response.status_code, 200)
        pass


if __name__ == '__main__':
    unittest.main()
