
import logging
from repositories import transaction_repository
from models import transaction_model
from logging.handlers import RotatingFileHandler
import streamlit as st

# RotatingFileHandler oluştur
handler = RotatingFileHandler(
    'logs/users.log', 
    maxBytes=1024*1024,  # 1 MB
    backupCount=3        # 3 yedek dosya
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Logger'ı al
logger = logging.getLogger("TransactionService")
logger.setLevel(logging.INFO)

# Handler'ı logger'a ekle
logger.addHandler(handler)

def perform_transaction(account_id: int, amount: float, transactions_type: str, kategori: str, descriptions: str = None):
    if not account_id:
        return False, "İşlem yapabilmek için önce bir hesaba giriş yapmalisiniz."
    
    try:
        transactions_id = transaction_repository.get_next_transaction_id()
        transaction = {
            "transactions_id": transactions_id,
            "account_id": account_id,
            "amount": amount,
            "transactions_type": transactions_type,
            "kategori": kategori,
            "descriptions": descriptions
        }
        transaction_repository.add_transaction(transaction)
        
        # Bakiyeyi güncelle
        if transactions_type == "para_yukle":
            transaction_repository.update_balance(account_id, amount, is_deposit=True)
        elif transactions_type in ["para_cek", "harcama"]:
            transaction_repository.update_balance(account_id, amount, is_deposit=False)
        
        logger.info(f"İşlem {transactions_id}: {transactions_type} {amount} TL başariyla gerçekleştirildi.")
        return True, f"{transactions_type} işlemi başariyla gerçekleştirildi."
    except ValueError as ve:
        logger.error(f"İşlem hatasi: {str(ve)}")
        return False, str(ve)
    except Exception as e:
        logger.error(f"İşlem sirasinda hata: {str(e)}")
        return False, f"İşlem sirasinda bir hata oluştu: {str(e)}"

def get_balance(account_id: int) -> float:                            #bakiyeyi al
    return transaction_repository.get_balance(account_id)

def get_transactions(account_id: int = None):
    return transaction_repository.get_transactions(account_id)

def get_categories_summary(account_id):
    gelir, harcama = transaction_repository.get_categories_summary(account_id) #transaction_repository.py den aldığı verileri sözlük formatına çevirir.
    kategoriler = []
    for row in gelir:
        kategoriler.append({
            "Tür": row[0],
            "Kategori": row[1],
            "İşlem Sayısı": row[2],
            "Toplam Tutar": f"{row[3]:.2f} TL"
        })
    for row in harcama:
        kategoriler.append({
            "Tür": row[0],
            "Kategori": row[1],
            "İşlem Sayısı": row[2],
            "Toplam Tutar": f"{row[3]:.2f} TL"
        })
    return kategoriler

def analyze_transactions(account_id: int, baslangic_str: str, bitis_str: str):
    result = transaction_repository.analyze_transactions(account_id, baslangic_str, bitis_str)
    analiz_sonuclari = []
    for row in result:
        analiz_sonuclari.append({
            "Kategori": row[0],
            "İşlem Sayısı": row[1],
            "Toplam Harcama": f"{row[2]:.2f} TL",
            "Ortalama Harcama": f"{row[3]:.2f} TL"
        })
    return analiz_sonuclari
