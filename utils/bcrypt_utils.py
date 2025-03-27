
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hash_pw = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_pw.decode('utf-8')

def verify_password(stored_hash: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash.encode('utf-8'))
