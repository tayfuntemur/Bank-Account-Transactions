# utils/validation_utils.py

import re

def id_validate(user_id: str) -> bool:
    return user_id and len(user_id.strip()) == 4 and user_id.isdigit()

def name_validate(name: str) -> bool:
    return bool(name and name.strip() and re.match(r'^[a-zA-ZğüşıöçĞÜŞİÖÇ\s]+$', name))

def email_validate(email: str) -> bool:
    return bool(email and email.strip() and re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def password_validate(password: str) -> bool:
    if not password or len(password) < 8:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*(),.?\":{}|<>" for c in password)
    return has_upper and has_lower and has_digit and has_special
