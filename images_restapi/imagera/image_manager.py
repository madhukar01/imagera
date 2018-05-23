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

    if not os.path.exists(folder):
        ans = ("Error", key)
        return ans
    else:
        images_list = ("Success", os.listdir(folder))
        return images_list


def validate_image(imgtype):
    """Function to validate image types"""
    if imgtype in image_types:
        return True
    else:
        return False


def store_image(inputkey, inputfile):
    """Function to store the uploaded image"""
    folder = storage + inputkey + "/" + inputfile.name

    if not os.path.exists(folder):
        default_storage.save(folder, inputfile)
        return True
    else:
        return False


def get_image_path(inputkey, inputName):
    """Function to get path of the image"""
    folder = storage + inputkey + "/" + inputName

    if not os.path.exists(folder):
        return False
    else:
        return folder


def update_image(inputkey, inputName, imagefile):
    """Function to replace existing image with uploaded image"""
    folder = get_image_path(inputkey, inputName)

    if folder is not False:
        try:
            os.remove(folder)
        except OSError:
            return False
        else:
            default_storage.save(folder, imagefile)
            return True
    else:
        return False


def delete_image(inputkey, inputName):
    """Function to delete image"""
    folder = get_image_path(inputkey, inputName)

    if folder is not False:
        try:
            os.remove(folder)
        except OSError:
            return False
        else:
            return True
    else:
        return False
