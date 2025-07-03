import hashlib
import string
import random


class PBKDF2:

    algorithm = hashlib.sha512().name
    iterations = 100000

    def encode(self, password: str, salt: str):
        assert password, 'password is obligatory'
        assert type(password) is str, 'password not is type str'
        assert salt, 'salt is obligatory'
        assert type(salt) is str, 'salt not is type str'
        password = hashlib.pbkdf2_hmac(self.algorithm, password.encode('utf-8'), salt.encode('utf-8'), self.iterations)
        return f'{self.algorithm}${self.iterations}${salt}${password.hex()}'


def get_random_string(length=70):
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_letters +
                                  string.ascii_lowercase, k=length))


def get_random_number(length=10):
    return ''.join(random.choices(string.digits, k=length))


def make_password(password: str, salt: str = None):
    salt = salt or get_random_string()
    pbkdf2 = PBKDF2()
    return pbkdf2.encode(password, salt)
