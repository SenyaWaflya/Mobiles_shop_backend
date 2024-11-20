import bcrypt


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    bytes_password = password.encode()
    return bcrypt.hashpw(bytes_password, salt)
