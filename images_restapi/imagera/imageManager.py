import os
from django.core.files.storage import default_storage

storage = '/image_storage/'
imageTypes = ['image/png', 'image/jpeg', 'image/gif']

"""
Functions to handle upload, retrieve, update and delete images
"""

def getImageList(key):
    """ Function to return images list of a access key """
    folder = storage + key

    if not os.path.exists(folder):
        ans = ("Error", key)
        return ans
        
    else:
        images_list = ("Success", os.listdir(folder))
        return images_list

def validateImage(imgType):
    """ Function to validate image types """
    if imgType in imageTypes:
        return True
    else:
        return False

def storeImage(inputKey, inputFile):
    """ Function to store the uploaded image """
    folder = storage + inputKey + inputFile.name

    if not os.path.exists(folder):
        default_storage.save(folder, inputFile)
        return True
    
    else:
        return False

def getImagePath(inputKey, inputName):
    """ Function to get path of the image """
    folder = storage + inputKey + inputName

    if not os.path.exists(folder):
        return False
    
    else:
        return folder

def updateImage(inputKey, inputName, imageFile):
    """ Function to replace existing image with uploaded image """
    folder = getImagePath(inputKey, inputName)

    if folder is not False:
        try:
            os.remove(folder)
        except OSError:
            return False
        else:
            default_storage.save(folder, imageFile)
            return True
    else:
        return False

def deleteImage(inputKey, inputName):
    """ Function to delete image """
    folder = getImagePath(inputKey, inputName)

    if folder is not False:
        try:
            os.remove(folder)
        except OSError:
            return False
        else:
            return True
    
    else:
        return False