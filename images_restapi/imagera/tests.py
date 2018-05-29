import ast
from django.test import TestCase, Client
import json
import shutil
import os


def byte_to_dict(bytearr):
    """
    Function to convert bytearray to json
    """
    my_dict = ast.literal_eval(bytearr.decode('utf-8'))
    return my_dict


class ImageraTest(TestCase):
    """
    Class to test image api
    """
    def setUp(self):
        self.client = Client()

        # Files for testing purpose
        self.storage = os.getcwd() + '/image_storage/'
        self.resourse = os.getcwd() + '/test_resource/'
        self.img1_path = self.resourse + 'dog1.jpg'
        self.img2_path = self.resourse + 'dog2.jpg'
        self.text_file = self.resourse + 'random.txt'

    def test_resource_files(self):
        self.assertEqual(os.path.exists(self.img1_path), True)
        self.assertEqual(os.path.exists(self.img2_path), True)

    def test_access_keys(self):

        # Send register request and get the key
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        responce_dict = byte_to_dict(response.content)
        key = responce_dict['Key']
        folder = self.storage + key

        # Check if the request has created folder for the key
        self.assertEqual(responce_dict['Message'],
                         'Access key generation successful !')
        self.assertEqual(os.path.exists(folder), True)

        # Send regenerate request and obtain new key
        response = self.client.post('/regenerate/', data={'key': key})
        self.assertEqual(response.status_code, 200)
        response_dict = byte_to_dict(response.content)
        old_key = key
        key = response_dict['Key']

        # Check if the previous folder has been renamed with new key
        self.assertNotEqual(os.path.exists(self.storage + old_key), True)
        self.assertEqual(response_dict['Message'],
                         "Access key regeneration successful !")
        self.assertEqual(os.path.exists(self.storage + key), True)

    def test_images(self):

        # Send register request and obtain a key
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)
        responce_dict = byte_to_dict(response.content)
        key = responce_dict['Key']

        # Send post request with text file and check for type mismatch
        with open(self.text_file, 'r') as fp:
            response = self.client.post('/imagelist/',
                                        data={'key': key, 'file': fp})
            self.assertEqual(response.status_code, 403)

        response_dict = byte_to_dict(response.content)
        self.assertEqual(response_dict['Message'],
                         "File type not supported")

        # Send post request with image and check if it is stored
        with open(self.img1_path, 'rb') as fp:
            response = self.client.post('/imagelist/',
                                        data={'key': key, 'file': fp})
            self.assertEqual(response.status_code, 201)
            response_dict = byte_to_dict(response.content)
            self.assertEqual(response_dict['Message'],
                             "Image uploaded successfully")

            # Send post request with same name and check if it returns error
            response = self.client.post('/imagelist/',
                                        data={'key': key, 'file': fp})
            self.assertEqual(response.status_code, 403)
            response_dict = byte_to_dict(response.content)
            self.assertEqual(response_dict['Message'],
                             "File name already exist")

        # Send get request and check if it returns name of uploaded images
        response = self.client.get('/imagelist/', data={'key': key})
        self.assertEqual(response.status_code, 200)
        responce_dict = byte_to_dict(response.content)
        self.assertEqual(responce_dict['Images'], 'dog1.jpg')

        # Send get request to view the image and check if it is success
        response = self.client.get('/imagedetail/',
                                   data={'key': key, 'name': 'dog1.jpg'})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):

        # Delete the files created during tests
        if os.path.exists(self.storage):
            shutil.rmtree(self.storage)
