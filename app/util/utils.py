from os import getenv
from os.path import isfile, join

UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")


def file_exist(filename):
    return isfile(join(UPLOAD_FOLDER, filename))
