
import sqlite3
from config import DB_NAME

def get_connection():
    return sqlite3.connect(DB_NAME)     #Sql bağlantısı

def create_transaction_tables():    #işlem tablosu oluşturma
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS transactions(
            transactions_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            transactions_type TEXT NOT NULL,
            kategori TEXT NOT NULL,
            descriptions TEXT,
            transactions_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(account_id) REFERENCES accounts(account_id)
        );
        """
    )
    conn.commit()
    conn.close()

def get_next_transaction_id():     # her yapılan işlemde sıralı işlem numarası ver.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(transactions_id) FROM transactions")
    max_id = cursor.fetchone()[0]
    conn.close()
    return 1 if max_id is None else max_id + 1

def add_transaction(transaction: dict):
    account_id = transaction["account_id"]
    current_balance = get_balance(account_id)

    # Yalnızca para çekme veya harcama işlemlerinde bakiye kontrolü yapılmalı
    if transaction["transactions_type"] in ["para_cek", "harcama"]:
        if transaction["amount"] > current_balance:
            raise ValueError(f"Insufficient balance. Current balance: {current_balance}, Transaction amount: {transaction['amount']}")

    # İşlem ekleme devamı...

    
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            """
            INSERT INTO transactions(
                transactions_id,
                account_id,
                amount,
                transactions_type,
                kategori,
                descriptions
            ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                transaction["transactions_id"],
                transaction["account_id"],
                transaction["amount"],
                transaction["transactions_type"],
                transaction["kategori"],
                transaction["descriptions"]
            )
        )
        
        conn.commit()
    except Exception as e:
        
        conn.rollback()
        raise e
    finally:
        conn.close()

def update_balance(account_id: int, amount: float, is_deposit: bool = True): # işlem yapıldığında bakiye güncelle.
    conn = get_connection()
    cursor = conn.cursor()
    if is_deposit:
        cursor.execute(
            "UPDATE accounts SET bakiye = bakiye + ? WHERE account_id = ?",
            (amount, account_id)
        )
    else:
        # Önce mevcut bakiyeyi kontrol etmek için
        cursor.execute("SELECT bakiye FROM accounts WHERE account_id = ?", (account_id,))
        current_balance = cursor.fetchone()[0]
        if current_balance < amount:
            conn.close()
            raise ValueError("Yetersiz bakiye.")
        cursor.execute(
            "UPDATE accounts SET bakiye = bakiye - ? WHERE account_id = ?",
            (amount, account_id)
        )
    conn.commit()
    conn.close()

def get_balance(account_id: int) -> float:
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT bakiye FROM accounts WHERE account_id = ?", (account_id,))
        result = cursor.fetchone()
        return result[0] if result else 0.0
    finally:
        conn.close()

def get_transactions(account_id: int = None): #Hesap numarasına ait yapılmış işlemleri getirir.
    conn = get_connection()
    cursor = conn.cursor()
    if account_id:
        cursor.execute("SELECT * FROM transactions WHERE account_id = ?", (account_id,))
    else:
        cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_categories_summary(account_id: int):    # hesabın gelir ve harcama kategorilerinin özetini çıkar.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 'Gelir' as type, kategori, COUNT(*) as islem_sayisi, SUM(amount) as toplam_tutar
        FROM transactions 
        WHERE transactions_type = 'para_yukle' 
        AND account_id = ?
        GROUP BY kategori
    """, (account_id,))
    gelir_kategorileri = cursor.fetchall()
    
    cursor.execute("""
        SELECT 'Harcama' as type, kategori, COUNT(*) as islem_sayisi, SUM(amount) as toplam_tutar
        FROM transactions 
        WHERE transactions_type = 'harcama' 
        AND account_id = ?
        GROUP BY kategori
    """, (account_id,))
    harcama_kategorileri = cursor.fetchall()
    
    conn.close()
    return gelir_kategorileri, harcama_kategorileri

def analyze_transactions(account_id: int, baslangic_tarihi: str, bitis_tarihi: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT kategori, COUNT(*) as islem_sayisi, SUM(amount) as toplam_harcama,
               AVG(amount) as ortalama_harcama
        FROM transactions 
        WHERE transactions_type = 'harcama'
        AND account_id = ?
        AND transactions_date BETWEEN ? AND ?
        GROUP BY kategori
        ORDER BY toplam_harcama DESC
    """, (account_id, baslangic_tarihi, bitis_tarihi))
    result = cursor.fetchall()
    conn.close()
    return result
