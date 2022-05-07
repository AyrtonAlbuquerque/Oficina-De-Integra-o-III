import jwt
from src.config import JWT_KEY

def generate_token(payload):
  return jwt.encode(payload, JWT_KEY, algorithm="HS256").decode('utf8')

def verify_token(token):
  try:
    decoded = jwt.decode(token, JWT_KEY, algorithms="HS256")
    return decoded
  except:
    return None