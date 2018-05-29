from django.core.files.storage import default_storage
import os

storage = os.getcwd() + '/image_storage/'
image_types = ['image/png', 'image/jpeg', 'image/gif']

"""
Functions to handle upload, retrieve, update and delete images
"""


def get_image_list(key):
    """Function to return images list of a access key"""
    folder = storage + key
    images_list = os.listdir(folder)
    return images_list


def validate_image(imgtype):
    """Function to validate image types"""
    if imgtype not in image_types:
        raise TypeError


def store_image(inputkey, inputfile):
    """Function to store the uploaded image"""
    folder = storage + inputkey + "/" + inputfile.name

    if not os.path.exists(folder):
        default_storage.save(folder, inputfile)
    else:
        raise FileExistsError


def get_image_path(inputkey, inputName):
    """Function to get path of the image"""
    folder = storage + inputkey + "/" + inputName

    if not os.path.exists(folder):
        raise FileNotFoundError
    else:
        return folder


def update_image(inputkey, inputName, imagefile):
    """Function to replace existing image with uploaded image"""
    folder = get_image_path(inputkey, inputName)
    os.remove(folder)
    default_storage.save(folder, imagefile)


def delete_image(inputkey, inputName):
    """Function to delete image"""
    folder = get_image_path(inputkey, inputName)
    os.remove(folder)
