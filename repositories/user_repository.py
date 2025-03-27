# repositories/user_repository.py

import sqlite3
from config import DB_NAME
import os

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():                    #Kullanıcı ve hesap tablosu oluştur.
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS accounts (
            user_id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            bakiye REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        """
    )
    conn.commit()
    conn.close()

def add_user(user: dict, crypted_password: str) -> None:        #Kullanıcı ekle
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO users(user_id, name, lastname, email, password)
        VALUES (?, ?, ?, ?, ?)
        """, (user["user_id"], user["name"], user["lastname"], user["email"], crypted_password)
    )
    # Otomatik hesap oluşturma
    account_id = int(user["user_id"]) * 10000 + 1
    cursor.execute(
        """
        INSERT INTO accounts(user_id, account_id, bakiye, created_at)
        VALUES (?, ?, ?, datetime('now'))
        """, (user["user_id"], account_id, 0.0)
    )
    conn.commit()
    conn.close()

def get_user(user_id: str):            #Kullanıcıyı getir
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

def get_account(user_id: str):     # kullanıcı hesabını getir
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT account_id FROM accounts WHERE user_id = ?", (user_id,))
    account_data = cursor.fetchone()
    conn.close()
    return account_data[0] if account_data else None
