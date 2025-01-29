import json
class JsonIsleyici:
    def __init__(self, dosya_adi=None):
        self.dosya_adi = dosya_adi
        self.veriler = None
        if dosya_adi:
            self.oku()

    def oku(self):
        try:
            with open(self.dosya_adi, 'r', encoding='utf-8') as f:
                self.veriler = json.load(f)
        except FileNotFoundError:
            print(f"Hata: {self.dosya_adi} dosyası bulunamadı.")
        except json.JSONDecodeError:
            print(f"Hata: {self.dosya_adi} dosyası geçerli bir JSON formatında değil.")

    def yaz(self, veriler):
        try:
            with open(self.dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(veriler, f, indent=4, ensure_ascii=False)
            print(f"Veriler {self.dosya_adi} dosyasına yazıldı.")
        except Exception as e:
            print(f"Hata: Veriler dosyaya yazılamadı: {e}")

    def verileri_getir(self):
        return self.veriler

    def veri_ekle(self, anahtar, deger):
        if self.veriler:
            self.veriler[anahtar] = deger
        else:
            print("Hata: Veriler henüz yüklenmedi.")

    def veri_guncelle(self, anahtar, deger):
        if self.veriler:
            if anahtar in self.veriler:
                self.veriler[anahtar] = deger
            else:
                print(f"Hata: {anahtar} anahtarı bulunamadı.")
        else:
            print("Hata: Veriler henüz yüklenmedi.")

    def veri_sil(self, anahtar):
        if self.veriler:
            if anahtar in self.veriler:
                del self.veriler[anahtar]
            else:
                print(f"Hata: {anahtar} anahtarı bulunamadı.")
        else:
            print("Hata: Veriler henüz yüklenmedi.")

def json_oku(dosya_adi):
    try:
        with open(dosya_adi, 'r', encoding='utf-8') as f:
            veriler = json.load(f)
            return veriler
    except FileNotFoundError:
        print(f"Hata: {dosya_adi} dosyası bulunamadı.")
        return None
    except json.JSONDecodeError:
        print(f"Hata: {dosya_adi} dosyası geçerli bir JSON formatında değil.")
        return None

def json_yaz(dosya_adi, veriler):
    try:
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            json.dump(veriler, f, indent=4, ensure_ascii=False)
        print(f"Veriler {dosya_adi} dosyasına yazıldı.")
    except Exception as e:
        print(f"Hata: Veriler dosyaya yazılamadı: {e}")

# Örnek kullanım
def demo():
    # JsonIsleyici sınıfını kullanarak
    isleyici = JsonIsleyici("veriler.json")
    isleyici.veri_ekle("yas", 30)
    isleyici.veri_guncelle("ad", "Ayşe")
    isleyici.veri_sil("soyad")
    isleyici.yaz(isleyici.veriler)

    # Fonksiyonları kullanarak
    veriler = json_oku("veriler.json")
    if veriler:
        print(veriler)
        veriler["sehir"] = "İstanbul"
        json_yaz("yeni_veriler.json", veriler)