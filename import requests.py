import requests
import time

# === KULLANICI AYARLARI ===
TELEGRAM_TOKEN = "8800549597:AAEVeeN9oGMFIIZpU88VZm8B8sT7RU1sDbA"
CHAT_ID = "969041165"
NEWS_API_KEY = "c6cec00f58434e3f861a27b20a27b39e"

# Takip edilecek anahtar kelimeler (İstediğin gibi ekleyip çıkarabilirsin)
ARANACAK_KELIMELER = ["Micron", "MU", "Trump", "MP Materials"]

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Mesaj gönderilemedi: {e}")

def haberleri_getir():
    print("Piyasa haberleri taranıyor...")
    bulunan_haberler = []
    
    # Belirlediğimiz kelimeleri NewsAPI üzerinde arıyoruz
    for kelime in ARANACAK_KELIMELER:
        # Son dakika haberlerini çekmek için sortBy=publishedAt kullanıyoruz
        url = f"https://newsapi.org/v2/everything?q={kelime}&language=en&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        try:
            cevap = requests.get(url).json()
            # Eğer API'den başarılı cevap geldiyse ve haber bulunduysa:
            if cevap.get("status") == "ok" and cevap.get("totalResults") > 0:
                en_yeni_haber = cevap["articles"][0]
                baslik = en_yeni_haber["title"]
                link = en_yeni_haber["url"]
                
                # Telegram mesaj şablonunu oluştur
                mesaj_metni = f"🔴 <b>Hedef:</b> {kelime}\n📰 <b>Haber:</b> {baslik}\n🔗 <a href='{link}'>Haberi Oku</a>"
                bulunan_haberler.append(mesaj_metni)
        except Exception as e:
            print(f"Haber çekilirken hata oluştu: {e}")
            
    return bulunan_haberler

if __name__ == "__main__":
    telegram_mesaj_gonder("🚀 Finans ve Makro Olay Botu aktif edildi. Taramalar başlıyor...")
    
    # Döngü sayesinde script kapanana kadar çalışmaya devam eder
    while True:
        yeni_haberler = haberleri_getir()
        for haber in yeni_haberler:
            telegram_mesaj_gonder(haber)
            time.sleep(2) # Telegram limitlerine takılmamak için 2 saniye es
        
        print("Tarama tamamlandı. Bir sonraki tarama için 1 saat bekleniyor...")
        time.sleep(3600) # Kodu 1 saat uyutur (3600 saniye)