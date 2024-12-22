import psycopg2

class Okul:
    def __init__(self, ogrenciler=None, personel=None, branslar=None, id=None):
        self.ogrenciler = ogrenciler
        self.personel = personel
        self.branslar = branslar
        self.id = id


class Ogrenciler(Okul):
    def __init__(self, id, ad, soyad, adres, tel, brans):
        super().__init__()
        self.id = id
        self.ad = ad
        self.soyad = soyad
        self.adres = adres
        self.tel = tel
        self.brans = brans


class Personel(Okul):
    def __init__(self, per_id, per_ad, per_soyad, per_adres, per_tel, per_brans):
        super().__init__()
        self.per_id = per_id
        self.per_ad = per_ad
        self.per_soyad = per_soyad
        self.per_adres = per_adres
        self.per_tel = per_tel
        self.per_brans = per_brans


class Otomasyon:
    def __init__(self):
        self.baglanti_ayarlari = {
            "dbname": "ogrenci_db",
            "user": "postgres",
            "password": "asd",
            "host": "localhost",
            "port": "5432",
        }
        self.connection = None  # Initialize connection to None
        self.cursor = None      # Initialize cursor to None
        self.baglanti_olustur()

    def baglanti_olustur(self):
        try:
            self.connection = psycopg2.connect(**self.baglanti_ayarlari)
            self.cursor = self.connection.cursor()
            self.tablo_olustur()
            print("Bağlantı başarılı")
        except psycopg2.Error as e:
            print("Bağlantı hatası: ", e)

    def tablo_olustur(self):
        try:
            # Check if the cursor has been initialized
            if self.cursor is not None:  
                self.cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ogrenciler(
                        id SERIAL PRIMARY KEY,
                        ad VARCHAR(50),
                        soyad VARCHAR(50),
                        adres VARCHAR(100),
                        tel VARCHAR(15),
                        brans VARCHAR(50)
                    );
                    CREATE TABLE IF NOT EXISTS personeller(
                        per_id SERIAL PRIMARY KEY,
                        per_ad VARCHAR(50),
                        per_soyad VARCHAR(50),
                        per_adres VARCHAR(100),
                        per_tel VARCHAR(15),
                        per_brans VARCHAR(50)
                    );
                    CREATE TABLE IF NOT EXISTS branslar(
                        br_id SERIAL PRIMARY KEY,
                        brans VARCHAR(50)
                    );
                    """
                )
                self.connection.commit()
            else:
                print("Cursor not initialized. Check database connection.")
        except psycopg2.Error as e:
            print("Tablo oluşturma hatası: ", e)

    def ogrenci_ekle(self, ad, soyad, adres, tel, brans):
        try:
            # Check if the cursor has been initialized
            if self.cursor is not None: 
                self.cursor.execute(
                    "INSERT INTO ogrenciler (ad, soyad, adres, tel, brans) VALUES (%s, %s, %s, %s, %s)",
                    (ad, soyad, adres, tel, brans),
                )
                self.connection.commit()
                print("Öğrenci eklendi.")
            else:
                print("Cursor not initialized. Check database connection.")
        except psycopg2.Error as e:
            print("Öğrenci ekleme hatası: ", e)

    def ogrenci_sil(self, id):
        try:
            # Check if the cursor has been initialized
            if self.cursor is not None:
                self.cursor.execute("DELETE FROM ogrenciler WHERE id = %s", (id,))
                self.connection.commit()
                print("Öğrenci silindi.")
            else:
                print("Cursor not initialized. Check database connection.")
        except psycopg2.Error as e:
            print("Öğrenci silme hatası: ", e)

    def ogrencileri_listele(self):
        try:
            # Check if the cursor has been initialized
            if self.cursor is not None:
                self.cursor.execute("SELECT * FROM ogrenciler")
                for ogrenci in self.cursor.fetchall():
                    print(ogrenci)
            else:
                print("Cursor not initialized. Check database connection.")
        except psycopg2.Error as e:
            print("Öğrencileri listeleme hatası: ", e)


otomasyon = Otomasyon()


def menu(secim):
    match secim:
        case "1":
            ad = input("Ad: ")
            soyad = input("Soyad: ")
            adres = input("Adres: ")
            tel = input("Tel: ")
            brans = input("Branş: ")
            otomasyon.ogrenci_ekle(ad, soyad, adres, tel, brans)
        case "2":
            id = int(input("Silmek istediğiniz öğrencinin id'si: "))
            otomasyon.ogrenci_sil(id)
        case "3":
            otomasyon.ogrencileri_listele()
        case "0":
            print("Çıkış yapılıyor...")
            return False
        case _:
            print("Hatalı seçim yaptınız...")
    return True


while True:
    print("\nÖğrenci Otomasyonu")
    print("1. Öğrenci Ekle")
    print("2. Öğrenci Sil")
    print("3. Öğrencileri Listele")
    print("0. Çıkış")
    secim = input("Seçiminizi yapınız: ")
    if not menu(secim):
        break