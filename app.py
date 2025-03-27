# app.py

import streamlit as st
from datetime import datetime, timedelta
from services import transaction_service, user_service
import os
from repositories import user_repository, transaction_repository
from services import user_service, transaction_service

# Gerekli tabloların oluşturulması (ilk çalıştırmada)
user_repository.create_tables()
transaction_repository.create_transaction_tables()


# Session state
if 'user_data' not in st.session_state:                  #oturum verileri başlat.
    st.session_state.user_data = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

def change_page(page):                            # giriş yaptıktan sonra kullanıcıyı ana sayfaya yönlendirmek için 
    st.session_state.page = page

def check_login():                                  #Giriş yapılmadıysa, kullanıcıyı giriş sayfasına yönlendir.
    if st.session_state.user_data is None:
        change_page('login')
        st.error("Önce giriş yapmalısınız!")
        return False
    return True

st.title("Banka Uygulaması")

if st.session_state.page == 'login':
    tab1, tab2 = st.tabs(["Giriş", "Kayıt Ol"])
    
    with tab1:
        st.header("Giriş Yap")
        user_id = st.text_input("Kullanıcı ID (4 haneli)", key="login_user_id")
        password = st.text_input("Şifre", type="password", key="login_password")
        
        if st.button("Giriş Yap"):
            if user_id and password:                                                      #kullanıcıyı ana sayfaya yönlendir..
                success, result = user_service.login_user(user_id, password)
                if success:
                    st.session_state.user_data = result
                    st.success(f"Hoş geldiniz, {result['name']} {result['lastname']}!")
                    change_page('dashboard')
                    st.rerun()
                else:
                    st.error(result)
            else:
                st.warning("Lütfen tüm alanları doldurun.")
    
    with tab2:
        st.header("Kayıt Ol")
        reg_user_id = st.text_input("Kullanıcı ID (4 haneli)", key="reg_user_id")
        reg_name = st.text_input("Ad", key="reg_name")
        reg_lastname = st.text_input("Soyad", key="reg_lastname")
        reg_email = st.text_input("E-posta", key="reg_email")
        reg_password = st.text_input("Şifre", type="password", help="En az 8 karakter, büyük/küçük harf, rakam ve özel karakter içermeli", key="reg_password")
        reg_password_confirm = st.text_input("Şifre (Tekrar)", type="password", key="reg_password_confirm")
        
        if st.button("Kayıt Ol"):
            if not all([reg_user_id, reg_name, reg_lastname, reg_email, reg_password, reg_password_confirm]):
                st.warning("Lütfen tüm alanları doldurun.")
            elif reg_password != reg_password_confirm:
                st.error("Şifreler eşleşmiyor!")
            else:
                success, message = user_service.register_user(reg_user_id, reg_name, reg_lastname, reg_email, reg_password)
                if success:
                    st.success(message)
                    st.info("Şimdi giriş yapabilirsiniz.")
                else:
                    st.error(message)
                    
elif st.session_state.page == 'dashboard':
    if not check_login():
        st.stop()
    
    user_data = st.session_state.user_data
    st.sidebar.title("Hoş geldiniz")
    st.sidebar.write(f"**Ad Soyad:** {user_data['name']} {user_data['lastname']}")
    st.sidebar.write(f"**Hesap ID:** {user_data['account_id']}")
    
    bakiye = transaction_service.get_balance(user_data['account_id'])
    st.sidebar.metric("Mevcut Bakiye", f"{bakiye:.2f} TL")
    
    if st.sidebar.button("Çıkış Yap"):
        st.session_state.user_data = None
        change_page('login')
        st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["İşlemler", "Geçmiş", "Analiz"])
    
    with tab1:
        st.header("Para İşlemleri")
        islem_tipi = st.selectbox("İşlem Türü", ["Para Yükle", "Para Çek", "Harcama Yap"])
        
        with st.form(key="transaction_form", clear_on_submit=True):
            miktar = st.number_input("Miktar (TL)", min_value=0.01, step=0.01, value=0.01, key="miktar_input")
            aciklama = st.text_area("Açıklama (İsteğe bağlı)", key="aciklama_input")
            kategori = None
            if islem_tipi == "Harcama Yap":
                kategori = st.selectbox("Kategori", ["Seçiniz", "Gıda", "Temizlik", "Kira", "Teknoloji", "Tekstil", "Sağlık", "Diğer"], key="kategori_input")
            submit_button = st.form_submit_button("İşlemi Gerçekleştir")
            
            if submit_button:
                if islem_tipi == "Para Yükle":
                    success, message = transaction_service.perform_transaction(user_data['account_id'], miktar, "para_yukle", "Gelir", aciklama)
                elif islem_tipi == "Para Çek":
                    success, message = transaction_service.perform_transaction(user_data['account_id'], miktar, "para_cek", "Nakit Çekim", aciklama)
                elif islem_tipi == "Harcama Yap":
                    if kategori == "Seçiniz":
                        st.error("Lütfen bir kategori seçin!")
                        success = False
                        message = "Kategori seçilmedi"
                    else:
                        success, message = transaction_service.perform_transaction(user_data['account_id'], miktar, "harcama", kategori, aciklama)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
                    
        bakiye = transaction_service.get_balance(user_data['account_id'])
        st.metric("Güncel Bakiye", f"{bakiye:.2f} TL")
    
    with tab2:
        st.header("İşlem Geçmişi")
        transactions = transaction_service.get_transactions(user_data['account_id'])
        if not transactions:
            st.info("Henüz işlem bulunmamaktadır.")
        else:
            data = []
            for t in transactions:
                data.append({
                    "ID": t[0],
                    "Tarih": t[6],
                    "İşlem Türü": t[3].replace("_", " ").title(),
                    "Kategori": t[4],
                    "Tutar": f"{t[2]:.2f} TL",
                    "Açıklama": t[5] or "-"
                })
            data = sorted(data, key=lambda x: x["ID"], reverse=True)
            st.dataframe(data)
    
    with tab3:
        st.header("İşlem Analizi")
        st.subheader("Kategori Özeti")
        kategori_ozeti = transaction_service.get_categories_summary(st.session_state.user_data['account_id'])


        if kategori_ozeti:
            st.dataframe(kategori_ozeti)
        else:
            st.info("Henüz kategori işlemi bulunmamaktadır.")
        
        st.subheader("Harcama Analizi")
        col1, col2 = st.columns(2)
        with col1:
            baslangic_tarihi = st.date_input("Başlangıç Tarihi", value=datetime.now() - timedelta(days=30))
        with col2:
            bitis_tarihi = st.date_input("Bitiş Tarihi",value=datetime.now())
        if st.button("Harcamaları Analiz Et"):
            bitis_str = bitis_tarihi.strftime('%Y-%m-%d 23:59:59')
            baslangic_str = baslangic_tarihi.strftime('%Y-%m-%d 00:00:00')
            account_id = user_data['account_id']
            harcama_analizi = transaction_service.analyze_transactions(account_id,baslangic_str, bitis_str)
            

            if harcama_analizi:
                harcama_analizi = sorted(harcama_analizi, key=lambda x: float(x['Toplam Harcama'].replace(' TL', '')), reverse=True)
                st.dataframe(harcama_analizi)
                en_fazla_harcama = harcama_analizi[0]
                st.success(f"En fazla harcama yapılan kategori: {en_fazla_harcama['Kategori']}")
            else:
                st.info("Belirtilen tarih aralığında harcama bulunmamaktadır.")
                
            