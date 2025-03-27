# services/user_service.py

import logging
from repositories import user_repository
from models import user_model
from utils import bcrypt_utils, validation_utils

logging.basicConfig(
    filename="logs/users.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("UserService")

def register_user(user_id: str, name: str, lastname: str, email: str, password: str):
    # Doğrulamalar
    if not validation_utils.id_validate(user_id):
        return False, "Geçersiz kullanıcı ID"
    if not validation_utils.name_validate(name):
        return False, "Geçersiz isim"
    if not validation_utils.name_validate(lastname):
        return False, "Geçersiz soyisim"
    if not validation_utils.email_validate(email):
        return False, "Geçersiz e-posta"
    if not validation_utils.password_validate(password):
        return False, "Geçersiz şifre"
    
    # Kullanıcının veritabanında olup olmadığını kontrol et
    if user_repository.get_user(user_id):
        return False, "Bu user_id zaten kullanılıyor."
    
    crypted_password = bcrypt_utils.hash_password(password)
    user = {
        "user_id": user_id,
        "name": name,
        "lastname": lastname,
        "email": email
    }
    
    try:
        user_repository.add_user(user, crypted_password)
        logger.info(f"Kullanıcı {name} {lastname} ({user_id}) başarıyla kaydedildi.")
        return True, f"Kullanıcı {name} {lastname} başarıyla kaydedildi."
    except Exception as e:
        logger.error(f"Kullanıcı ekleme hatası: {str(e)}")
        return False, f"Kullanıcı ekleme hatası: {str(e)}"

def login_user(user_id: str, password: str):
    user_data = user_repository.get_user(user_id)
    if not user_data:
        logger.warning(f"Giriş başarısız: {user_id} ID'li kullanıcı bulunamadı.")
        return False, "Kullanıcı bulunamadı."
    stored_hash = user_data[4]
    if bcrypt_utils.verify_password(stored_hash, password):
        account_id = user_repository.get_account(user_id)
        if account_id:
            logger.info(f"Kullanıcı {user_id} başarılı giriş yaptı.")
            return True, {
                "user_id": user_id,
                "name": user_data[1],
                "lastname": user_data[2],
                "account_id": account_id
            }
        else:
            return False, "Hesap bilgileri bulunamadı."
    else:
        logger.warning(f"Kullanıcı {user_id} için şifre doğrulaması başarısız oldu.")
        return False, "Geçersiz şifre."
