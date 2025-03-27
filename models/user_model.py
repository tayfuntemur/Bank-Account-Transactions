from dataclasses import dataclass

@dataclass
class User:
    user_id: str
    name: str
    lastname: str
    email: str
    password: str  # Şifreli hali
