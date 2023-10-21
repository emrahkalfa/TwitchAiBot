import csv
import os

class Leaderboard:
    def __init__(self, dosya_adi):
        self.dosya_adi = dosya_adi
        self.izleyiciler = {}
        self._dosya_kontrol()
        self._verileri_oku()



    def _dosya_kontrol(self):
        if not os.path.isfile(self.dosya_adi):
            with open(self.dosya_adi, mode='w', newline='') as dosya:
                yazici = csv.writer(dosya)
                yazici.writerow(["Follower", "Score"])


    def _verileri_oku(self):
        try:
            with open(self.dosya_adi, mode='r', newline='') as dosya:
                okuyucu = csv.reader(dosya)
                for satir in okuyucu:
                    ad, miktar = satir
                    self.izleyiciler[ad] = int(miktar)
        except FileNotFoundError:
            pass

    def _verileri_yaz(self):
        with open(self.dosya_adi, mode='w', newline='') as dosya:
            yazici = csv.writer(dosya)
            for ad, miktar in self.izleyiciler.items():
                yazici.writerow([ad, miktar])

    def urun_ekle(self, ad, miktar):
        if ad in self.izleyiciler:
            self.izleyiciler[ad] += miktar
        else:
            self.izleyiciler[ad] = miktar
        self._verileri_yaz()

   
    def stok_goruntule(self):
        for ad, miktar in self.izleyiciler.items():
            print(f"Ürün Adı: {ad}, Miktar: {miktar}")


LB = Leaderboard("lb.csv")


LB.urun_ekle("Silgi", 200)


# Stoktaki ürünleri görüntülemek için kullanım örneği
LB.stok_goruntule()