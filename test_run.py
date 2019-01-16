# import os
import unittest

from run import app

class BasicTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass 


    @classmethod
    def tearDownClass(cls):
        pass 

    # SETUP and TEARDOWN
    def setUp(self):
        pass

    def tearDown(self):
        pass

    # TESTS

    def test_get_routes_no_params(self):
        tester = app.test_client(self)

        response = tester.get('/', content_type="html/text")
        self.assertEqual(response.status_code, 200)

        response = tester.get('/get_food_items', content_type="html/text")
        self.assertEqual(response.status_code, 200)

        response = tester.get('/add_food_item', content_type="html/text")
        self.assertEqual(response.status_code, 200)

        response = tester.get('/get_classification', content_type="html/text")
        self.assertEqual(response.status_code, 200)

        response = tester.get('/add_class', content_type="html/text")
        self.assertEqual(response.status_code, 200)

        response = tester.get('/dashboard', content_type="html/text")
        self.assertEqual(response.status_code, 200)

        response = tester.get('/about', content_type="html/text")
        self.assertEqual(response.status_code, 200)

        response = tester.get('/contact', content_type="html/text")
        self.assertEqual(response.status_code, 200)



    def test_get_routes_no_params_connect_to_correct_template(self):
        tester = app.test_client(self)

        response = tester.get('/', content_type="html/text")
        self.assertTrue(b'Nutrition Value App' in response.data)

        response = tester.get('/get_food_items', content_type="html/text")
        self.assertTrue(b'Click to check the details of each food item' in response.data)

        response = tester.get('/add_food_item', content_type="html/text")
        self.assertTrue(b'Add the details for the food item you want to add and click the "Add" button' in response.data)

        response = tester.get('/get_classification', content_type="html/text")
        self.assertTrue(b'The following is a list of food classifications in this data set' in response.data)

        response = tester.get('/add_class', content_type="html/text")
        self.assertTrue(b'Add a Food Class' in response.data)

        response = tester.get('/dashboard', content_type="html/text")
        self.assertTrue(b'Dashboard' in response.data)

        response = tester.get('/about', content_type="html/text")
        self.assertTrue(b'About this App' in response.data)

        response = tester.get('/contact', content_type="html/text")
        self.assertTrue(b'Contact Us' in response.data)

if __name__ == "__main__":
    unittest.main()