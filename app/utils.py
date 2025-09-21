# app/utils.py
from passlib.context import CryptContext
from textblob import TextBlob
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def analyze_sentiment(text: str) -> str:
    """Returns 'positive' or 'negative' based on sentiment polarity."""
    blob = TextBlob(text)
    return "positive" if blob.sentiment.polarity >= 0 else "negative"