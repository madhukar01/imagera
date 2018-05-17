from random import choice
from string import ascii_letters, digits
import os
storage = '/image_storage/'

"""
Functions to manage access keys and respective folders
"""

def genKey():
    """ Function to generate a new access key which does not exist already """
    key = ''.join(choice(ascii_letters + digits) for _ in range(16))

    while(validateKey(key)):
        key = ''.join(choice(ascii_letters + digits) for _ in range(16))

    return key


def validateKey(key):
    """ Function to validate access key """
    folder = storage + key

    if(os.path.exists(folder)):
        return True
    else:
        return False


def generateKeyCreateFolder():
    """ Function to create folders for newly generated access key """
    key = genKey()
    folder = storage + key
    os.makedirs(folder)
    return key
        

def reGenerateKey(key):
    """ Function to regenerate the currently existing access key and rename the folder """
    key = key.strip()

    if not validateKey(key):
        return ("Error", key)
        
    else:
        folder = storage + key
        newKey = genKey()
        newFolder = storage + newKey
        os.rename(folder, newFolder)
        return ("Success", newKey)

            
            


