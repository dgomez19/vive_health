import random
import string
import re


def random_password(length):

    character = string.ascii_letters + string.digits
    password = ''

    for _ in range(length):
        password += random.choice(character)

    return password


def validate_password(password):
    pattern = re.compile(r'(?=.*[a-zñáéíóú])(?=.*[A-ZÑÁÉÍÓÚÜ])(?=.*\d)(?=.*[!"#$%&\'()*+,\-./:;<=>?@[\\\]^_¿`{|}~])'
                         r'[A-ZÑÁÉÍÓÚÜa-zñáéíóú\d!"#$%&\'()*+,\-./:;<=>?@[\\\]^_¿`{|}~]')

    return True if pattern.search(password) else False
