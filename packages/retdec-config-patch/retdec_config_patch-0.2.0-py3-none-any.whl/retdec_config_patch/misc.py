# IMPORTS
import hashlib
import os
import random
import string


# FUNCTIONS
def gen_random_string(length: int = 8) -> str:
    """
    Generates a random string of the desired length.

    :param length: length of string to generate, defaults to 8
    :return: a random string
    """

    return "".join(random.choices(string.ascii_letters, k=length))


def get_file_hash(file: os.PathLike) -> str:
    """
    Gets the SHA256 hash of the file.

    :param file: file to get the hash of
    :return: hash of the file
    """
    
    with open(file, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
