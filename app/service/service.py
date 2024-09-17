from jose import JWTError, jwt
from passlib.context import CryptContext
password_context = CryptContext(schemes=["bcrypt"])

# def verify_password(password: str, hashed_password: str):
#     return password_context.verify(password, hashed_password)


# def get_password_hash(password: str) -> str:
#     return password_context.hash(password)
