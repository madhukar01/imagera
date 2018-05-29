import os
from random import choice
from string import ascii_letters, digits

storage = os.getcwd() + '/image_storage/'

"""
Functions to manage access keys and respective folders
"""


def gen_key():
    """Function to generate a new access key which does not exist already"""
    key = ''.join(choice(ascii_letters + digits) for _ in range(16))
    folder = storage + key

    while(os.path.exists(folder)):
        key = ''.join(choice(ascii_letters + digits) for _ in range(16))
        folder = storage + key
    return key


def validate_key(key):
    """Function to validate access key"""
    folder = storage + key

    if not os.path.exists(folder):
        raise FileNotFoundError


def generate_key_create_folder():
    """Function to create folders for newly generated access key"""
    key = gen_key()
    folder = storage + key
    os.makedirs(folder)
    return key


def regenerate_key(key):
    """
    Function to regenerate the currently existing
    access key and rename the folder
    """
    key = key.strip()
    folder = storage + key
    newkey = gen_key()
    newfolder = storage + newkey
    os.rename(folder, newfolder)
    return newkey
