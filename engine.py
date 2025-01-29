import os,json,time,sqlite3 
import json_ENGİNE as jet
import sql_engine as sql

if os.path.exists("ayarlar.json"):
    ayarlar = jet.JsonIsleyici("ayarlar.json")
    jsondata = jet.json_oku("ayarlar.json")

    if jsondata == None:
        ayarlar.yaz({"veritabani_adi": "kutuphane.db","en_last_id": 0,"tr_last_id": 0})
    else:
        if "veritabani_adi" not in jsondata:        
            ayarlar.yaz({"veritabani_adi": "kutuphane.db"})
        if "en_last_id" not in jsondata:
            ayarlar.yaz({"en_last_id": 0})
        if "tr_last_id" not in jsondata:
            ayarlar.yaz({"tr_last_id": 0})
    jsondata = jet.json_oku("ayarlar.json")


else:
    ayarlar = jet.JsonIsleyici()
    ayarlar.dosya_adi = "ayarlar.json"
    ayarlar.veri_ekle("veritabani_adi", "kutuphane.db")
    ayarlar.yaz({"veritabani_adi": "kutuphane.db","en_last_id": 0,"tr_last_id": 0})
    jsondata = ayarlar.oku()

print(jsondata)
database = sql.Veritabani("kutuphane.db")
database.baglan()
database.tablo_olustur("en_kelimeler", [ "kelime TEXT DEFAULT 'varsayilan'", "anlam TEXT DEFAULT 'varsayilan'", "t1 TEXT DEFAULT 'varsayilan'","t2 TEXT DEFAULT 'varsayilan'","t3 TEXT DEFAULT 'varsayilan'","t4 TEXT DEFAULT 'varsayilan'","dogru_cevap TEXT DEFAULT 'varsayilan'"])
database.tablo_olustur("tr_kelimeler", [ "kelime TEXT DEFAULT 'varsayilan'", "anlam TEXT DEFAULT 'varsayilan'", "t1 TEXT DEFAULT 'varsayilan'","t2 TEXT DEFAULT 'varsayilan'","t3 TEXT DEFAULT 'varsayilan'","t4 TEXT DEFAULT 'varsayilan'","dogru_cevap TEXT DEFAULT 'varsayilan'"])

raw_word = open("EN-WORDS/raw.txt","r",encoding="utf-8").read().split("\n")
print(len(raw_word))
e_count = 0
for i in raw_word:
    database.veri_ekle("en_kelimeler", ["kelime","anlam"], (i,"2"))
    e_count += 1
    
    percent = int((e_count/len(raw_word))*10000)/100
    print(f"{e_count}/{len(raw_word)} - %{percent} complated")
    
database.baglantiyi_kes()
