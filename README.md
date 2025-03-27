[![](https://icons8.com/icon/43128/bank)] # Bank-Account-Transactions
Banka Uygulaması, kullanıcıların hesap bilgilerini yönetebileceği, işlem yapabileceği ve harcama analizleri yapabileceği bir platformdur. 
Kullanıcılar, para yatırma, çekme, harcama yapma işlemlerini gerçekleştirebilir ve bu işlemler üzerinden finansal analizler alabilirler.

## Özellikler:
- Kullanıcı Girişi ve Kayıt: Kullanıcılar, kendi hesaplarını oluşturup giriş yapabilirler.
- Para İşlemleri: Kullanıcılar, hesaplarına para yükleyebilir, para çekebilir ve harcama yapabilirler.
- İşlem Geçmişi: Kullanıcılar, geçmiş işlemlerini görüntüleyebilirler.
- Kategori Özeti: Kullanıcıların yaptığı işlemlerin kategori bazında özeti alınabilir.
- Harcama Analizi: Belirli bir tarih aralığında yapılan harcamalar analiz edilebilir.

## Mimari
### Katmanlı (layered) Mimari
Banka_uygulamasi/
│
- ├── app.py                     #Ana giriş noktası (Streamlit UI)
- ├── config.py                  #Yapılandırma ayarları (örneğin, veritabanı adı, log ayarları)
├── requirements.txt           #Gerekli kütüphaneler
│
├── services/                  #İş mantığı katmanı
│   ├── user_service.py        #Kullanıcı işlemleri
│   ├── transaction_service.py #İşlem işlemleri
│
├── repositories/              #Veri erişim katmanı
│   ├── user_repository.py     #Kullanıcı veritabanı işlemleri
│   ├── transaction_repository.py #İşlem veritabanı işlemleri
│
├── models/                    #Model katmanı
│   ├── user_model.py          #Kullanıcı modeli
│   ├── transaction_model.py   #İşlem modeli
│
├── utils/                     #Yardımcı fonksiyonlar
│   ├── bcrypt_utils.py        #Şifreleme işlemleri
│   ├── validation_utils.py    #Doğrulama işlemleri
│
└── logs/                      #Log dosyaları
    └── users.log              #Kullanıcı logları

## Teknolojiler:
-Streamlit: Web arayüzü için kullanılmıştır.
-SQLite: Veritabanı olarak kullanılmıştır.
-Python: Uygulamanın temel programlama dili.
-Logging: Uygulama içi işlem ve hata takibi için kullanılmıştır.

## Başlangıç:
Gereksinimler
Python 3.7+
Streamlit
SQLite (Veritabanı)

## Kurulum:
### Gerekli Kütüphanelerin Yüklenmesi:
Aşağıdaki komutla gerekli Python paketlerini yükleyin:
bashCopypip install -r requirements.txt

## Veritabanı Kurulumu:
Uygulama ilk başlatıldığında gerekli veritabanı tabloları otomatik olarak oluşturulacaktır. 
Bunun için repositories dizininde bulunan user_repository.py ve transaction_repository.py dosyalarını çalıştırabilirsiniz.

## Veritabanı Kurulumu:
### Uygulamanın Başlatılması
Uygulamanızı başlatmak için aşağıdaki komutu çalıştırabilirsiniz:
bashCopystreamlit run app.py
Bu komut, uygulamanızı yerel bir sunucuda başlatacak ve tarayıcınızda açacaktır.

## Kullanım
### Kullanıcı Girişi ve Kayıt
Uygulamaya giriş yapabilir ya da yeni bir kullanıcı kaydı oluşturabilirsiniz.
### İşlem Yapma
Kullanıcılar, hesaplarına para yükleyebilir, para çekebilir veya harcama yapabilirler.
### İşlem Geçmişi ve Analiz
Kullanıcılar geçmiş işlemlerini görüntüleyebilir ve belirli tarih aralıklarında yapılan harcamalarla ilgili analizler alabilirler.
### Kategori Özeti
Yaptığınız işlemler kategorilere ayrılarak toplam harcama ve gelir kategorileri sunulur.
### Harcama Analizi
Belirli bir tarih aralığında yapılan harcamaların analizi yapılır ve en fazla harcama yapılan kategoriyi gösterir.
### Katkı
Eğer bu projeye katkıda bulunmak isterseniz, aşağıdaki adımları takip edebilirsiniz:

## Projeyi forklayın.
Yapmak istediğiniz değişiklikleri gerçekleştirin.
Değişikliklerinizi bir pull request olarak gönderin.

## Lisans
Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakabilirsiniz.
