<?php

class SQLiteVeritabani
{
    private $db;

    public function __construct($veritabaniDosyasi)
    {
        try {
            $this->db = new PDO("sqlite:" . $veritabaniDosyasi);
            $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            die("Veritabanı bağlantı hatası: " . $e->getMessage());
        }
    }

    public function __destruct()
    {
        $this->db = null;
    }

    public function veriEkle($tablo, $veriler)
    {
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

    public function veriGetir($tablo, $kosul = null)
    {
        $sql = "SELECT * FROM " . $tablo;
        if ($kosul) {
            $sql .= " WHERE " . $kosul;
        }
        $stmt = $this->db->query($sql);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    public function veriGuncelle($tablo, $veriler, $kosul)
    {
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

    public function veriSil($tablo, $kosul)
    {
        $sql = "DELETE FROM " . $tablo . " WHERE " . $kosul;
        $stmt = $this->db->exec($sql);
        return $stmt;
    }
}


function connectToDatabase($dbFilePath)
{
    try {
        // SQLite veritabanına bağlan
        $db = new PDO("sqlite:" . $dbFilePath);
        // Hata modunu ayarla
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        return $db;
    } catch (PDOException $e) {
        // Hata mesajını göster
        echo "Veritabanına bağlanırken hata oluştu: " . $e->getMessage();
        exit();
    }
}

// Tablo oluştur
function createTable($db, $tableName, $columns)
{
    // SQL sorgusunu hazırla
    $sql = "CREATE TABLE IF NOT EXISTS $tableName ($columns)";
    // Sorguyu çalıştır
    $db->exec($sql);
}

// Veri ekle
function insertData($db, $tableName, $columns, $values)
{
    // Kolonları ve değerleri virgülle ayırarak birleştir
    $columnsStr = implode(", ", $columns);
    $placeholders = implode(", ", array_fill(0, count($values), '?'));
    // SQL sorgusunu hazırla
    $sql = "INSERT INTO $tableName ($columnsStr) VALUES ($placeholders)";
    // Sorguyu çalıştır
    $stmt = $db->prepare($sql);
    $stmt->execute($values);
}

// Veri çek
function fetchData($db, $query)
{
    // Sorguyu çalıştır ve sonuçları al
    $stmt = $db->query($query);
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    return $rows;
}
function singleFetchData($db, $query)
{
    // Sorguyu çalıştır ve sonuçları al
    $stmt = $db->query($query);
    $rows = $stmt->fetch(PDO::FETCH_ASSOC);
    return $rows;
}

// Veri güncelle
function updateData($db, $tableName, $set, $where)
{
    // SQL sorgusunu hazırla
    $sql = "UPDATE $tableName SET $set WHERE $where";
    // Sorguyu çalıştır
    $db->exec($sql);
}

// Veri sil
function deleteData($db, $tableName, $where)
{
    // SQL sorgusunu hazırla
    $sql = "DELETE FROM $tableName WHERE $where";
    // Sorguyu çalıştır
    $db->exec($sql);
}

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <title>Bootstrap 5 Example</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</head>

<body>

    <div class="container-fluid p-5 bg-primary text-white text-center">
        <h1>ENGLISH WordLİST</h1>
        <p></p>
    </div>

    <div class="container mt-5">
        <table>
            <thead>
                <tr>
                    <th>id</th>
                    <th>word</th>
                    <th>meaning</th>
                    <th>example</th>
                </tr>
            </thead>
            <tbody>
                <?php
                $db = connectToDatabase("kutuphane.db");
                $result = fetchData($db, "SELECT * FROM en_kelimeler");
                foreach ($result as $key => $row) {
                    echo "<tr>";
                    echo "<td>" . $row["kelime"] . "</td>";
                    echo "<td>" . $row["anlam"] . "</td>";
                    echo "<td>" . $row["t1"] . "</td>";
                    echo "<td>" . $row["t2"] . "</td>";
                    echo "</tr>";
                }
                while ($row = $result->fetchArray()) {
                    
                };
                ?>
            </tbody>
        </table>
    </div>

</body>

</html>