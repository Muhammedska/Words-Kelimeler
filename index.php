<?php

class SQLiteVeritabani {
    private $db;

    public function __construct($veritabaniDosyasi) {
        try {
            $this->db = new PDO("sqlite:" . $veritabaniDosyasi);
            $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            die("Veritabanı bağlantı hatası: " . $e->getMessage());
        }
    }

    public function __destruct() {
        $this->db = null;
    }

    public function veriEkle($tablo, $veriler) {
        $sutunlar = implode(",", array_keys($veriler));
        $degerler = ":" . implode(",:", array_keys($veriler));
        $sql = "INSERT INTO " . $tablo . " (" . $sutunlar . ") VALUES (" . $degerler . ")";
        $stmt = $this->db->prepare($sql);
        foreach ($veriler as $anahtar => $deger) {
            $stmt->bindValue(":" . $anahtar, $deger);
        }
        $stmt->execute();
        return $this->db->lastInsertId();
    }

    public function veriGetir($tablo, $kosul = null) {
        $sql = "SELECT * FROM " . $tablo;
        if ($kosul) {
            $sql .= " WHERE " . $kosul;
        }
        $stmt = $this->db->query($sql);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    public function veriGuncelle($tablo, $veriler, $kosul) {
        $guncellemeler = [];
        foreach ($veriler as $anahtar => $deger) {
            $guncellemeler[] = $anahtar . " = :" . $anahtar;
        }
        $sql = "UPDATE " . $tablo . " SET " . implode(",", $guncellemeler) . " WHERE " . $kosul;
        $stmt = $this->db->prepare($sql);
        foreach ($veriler as $anahtar => $deger) {
            $stmt->bindValue(":" . $anahtar, $deger);
        }
        $stmt->execute();
        return $stmt->rowCount();
    }

    public function veriSil($tablo, $kosul) {
        $sql = "DELETE FROM " . $tablo . " WHERE " . $kosul;
        $stmt = $this->db->exec($sql);
        return $stmt;
    }
}

?>