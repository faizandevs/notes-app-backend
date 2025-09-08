from passlib.context import CryptContext

# 1. Create a password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Function to hash a plain password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 3. Function to verify a plain password against the hashed one
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
