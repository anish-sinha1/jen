import bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import HashingError

from strenum import StrEnum

from app.log.logger import get_logger
from app.util.enum_base import EnumBase

logger = get_logger("Algorithms")


class HashAlgorithm(StrEnum, metaclass=EnumBase):
    """List of password hashing algorithms supported by the application"""

    ARGON2 = "argon2"
    BCRYPT = "bcrypt"


def hash_argon2(password: str) -> str | None:
    """Hash a password with the argon2 algorithm

    :param password: the password to hash
    :return: the hashed password or None
    """
    try:
        hasher = PasswordHasher()
        return hasher.hash(password)
    except HashingError as e:
        logger.error(str(e))
        return None


# TODO: Remove bare except and fix bcrypt type hints
def hash_bcrypt(password: str) -> str | None:
    """Hash a password with the bcrypt algorithm

    :param password: the password to hash
    :return: the hashed password or None
    """
    try:
        return bcrypt.hashpw(password, bcrypt.gensalt())
    except:  # nolint
        return None


# TODO: Remove bare except
def verify_argon2(hashed: str, candidate: str) -> bool:
    """Verify a hash generated by argon2

    :param hashed: the hashed password
    :candidate: what we should compare with
    """
    try:
        hasher = PasswordHasher()
        return hasher.verify(hashed, candidate)
    except:
        return False


def verify_bcrypt(hashed: str, candidate: str) -> bool:
    """Verify a hash generated by bcrypt

    :param hashed: the hashed password
    :candidate: what we should compare with
    """
    try:
        return bcrypt.checkpw(candidate, hashed)
    except:
        return False
