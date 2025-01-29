import sqlite3
class Veritabani:
    def __init__(self, veritabani_adi):
        self.veritabani_adi = veritabani_adi
        self.conn = None
        self.cursor = None

    def baglan(self):
        try:
            self.conn = sqlite3.connect(self.veritabani_adi)
            self.cursor = self.conn.cursor()
            print("Veritabanına bağlandı.")
        except sqlite3.Error as e:
            print(f"Veritabanına bağlanırken hata oluştu: {e}")

    def baglantiyi_kes(self):
        if self.conn:
            self.conn.close()
            print("Veritabanı bağlantısı kesildi.")

    def tablo_olustur(self, tablo_adi, sutunlar):
        try:
            sorgu = f"CREATE TABLE IF NOT EXISTS {tablo_adi} ({', '.join(sutunlar)})"
            self.cursor.execute(sorgu)
            self.conn.commit()
            print(f"{tablo_adi} tablosu oluşturuldu.")
        except sqlite3.Error as e:
            print(f"Tablo oluşturulurken hata oluştu: {e}")

    def veri_ekle(self, tablo_adi, sutunlar, veriler):
        try:
            sorgu = f"INSERT INTO {tablo_adi} ({', '.join(sutunlar)}) VALUES ({', '.join(['?'] * len(sutunlar))})"
            self.cursor.execute(sorgu, veriler)
            self.conn.commit()
            print("Veri eklendi.")
        except sqlite3.Error as e:
            print(f"Veri eklenirken hata oluştu: {e}")

    def verileri_getir(self, tablo_adi, kosul=None):
        try:
            sorgu = f"SELECT * FROM {tablo_adi}"
            if kosul:
                sorgu += f" WHERE {kosul}"
            self.cursor.execute(sorgu)
            veriler = self.cursor.fetchall()
            return veriler
        except sqlite3.Error as e:
            print(f"Veriler getirilirken hata oluştu: {e}")
            return None

    def verileri_guncelle(self, tablo_adi, sutun_degerleri, kosul):
        try:
            sorgu = f"UPDATE {tablo_adi} SET {', '.join([f'{sutun} = ?' for sutun in sutun_degerleri])} WHERE {kosul}"
            self.cursor.execute(sorgu, list(sutun_degerleri.values()))
            self.conn.commit()
            print("Veriler güncellendi.")
        except sqlite3.Error as e:
            print(f"Veriler güncellenirken hata oluştu: {e}")

    def verileri_sil(self, tablo_adi, kosul):
        try:
            sorgu = f"DELETE FROM {tablo_adi} WHERE {kosul}"
            self.cursor.execute(sorgu)
            self.conn.commit()
            print("Veriler silindi.")
        except sqlite3.Error as e:
            print(f"Veriler silinirken hata oluştu: {e}")

def demo():
    # Örnek kullanım
    veritabani = Veritabani("veritabani.db")
    veritabani.baglan()

    veritabani.tablo_olustur("ogrenciler", ["id INTEGER PRIMARY KEY AUTOINCREMENT", "ad TEXT NOT NULL", "soyad TEXT NOT NULL", "yas INTEGER"])


    veriler = veritabani.verileri_getir("ogrenciler")
    if veriler:
        for veri in veriler:
            print(veri)

    veritabani.verileri_guncelle("ogrenciler", {"yas": 21}, "ad = 'Ali'")

    #veritabani.verileri_sil("ogrenciler", "ad = 'Ali'")

    veritabani.baglantiyi_kes()