# 🎙️ Audio Transcriber

Windows için ses kayıt ve transkripsiyon uygulaması. Mikrofon ve sistem sesini kaydeder, 10 dakikalık bloklara ayırır, Gladia ile transkript eder ve Gemini AI ile not çıkarır.

## ✨ Özellikler

- 🎤 **Çoklu Ses Kaydı** - Mikrofon + Sistem sesi aynı anda
- 📦 **Akıllı Bloklama** - 10 dk'lık parçalar (maliyet optimizasyonu)
- 🎮 **Blok Oynatma** - Her bloğu dinleyerek inceleme
- ✅ **Esnek Seçim** - İstediğin blokları seçip çevir
- 📝 **Gladia Transkripsiyon** - Yüksek doğruluklu Türkçe çeviri
- 🤖 **Gemini AI Notları** - Otomatik not çıkarma
- 💾 **Markdown Export** - Notları kaydet ve paylaş
- 🎨 **Modern UI** - CustomTkinter ile profesyonel arayüz

## 🚀 Kurulum

### 1. Python Ortamı

```bash
# Proje klasörünü klonla
git clone https://github.com/yourusername/audio_transcriber.git
cd audio_transcriber

# Virtual environment (önerilir)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2. API Anahtarları

**Gladia API Key:**
1. https://app.gladia.io/ adresine git
2. Ücretsiz hesap oluştur
3. Dashboard'dan API key al

**Gemini API Key:**
1. https://aistudio.google.com/apikey adresine git
2. Google hesabınla giriş yap
3. API key oluştur

### 3. Konfigürasyon

`.env.example` dosyasını `.env` olarak kopyala ve API anahtarlarını ekle:

```bash
cp .env.example .env
```

`.env` dosyasını düzenle:

```env
GLADIA_API_KEY=your-gladia-key-here
GEMINI_API_KEY=your-gemini-key-here
```

Veya environment variable olarak ayarla:

```bash
# Windows
set GLADIA_API_KEY=your-key
set GEMINI_API_KEY=your-key

# Linux/Mac
export GLADIA_API_KEY=your-key
export GEMINI_API_KEY=your-key
```

## 📖 Kullanım

### Uygulamayı Başlat

```bash
python main.py
```

### İş Akışı

1. **Kaynak Seç** - Mikrofon ve/veya Sistem Sesi
2. **Kayda Başla** - ⏺️ butonuna tıkla
3. **Kaydet** - Otomatik 10 dk bloklar oluşur
4. **Kaydı Durdur** - ⏹️ butonuna tıkla
5. **Blokları Dinle** - ▶️ butonuyla her bloğu önizle
6. **Blok Seç** - Transkript etmek istediklerini seç
7. **Çevir** - "Seçilenleri Çevir" butonuna tıkla
8. **Not Çıkar** - "Gemini ile Not Çıkar" butonuna tıkla
9. **Kaydet** - Notları markdown olarak dışa aktar

## 💰 Maliyet Tahmini

| Servis | Birim Fiyat | 10 dk | 1 saat |
|--------|-------------|-------|--------|
| Gladia | ~$0.0002/sn | ~$0.12 | ~$0.70 |
| Gemini Flash | Ücretsiz* | $0 | $0 |

*Gemini 2.5 Flash günlük ücretsiz limit içinde.

## 📁 Proje Yapısı

```
audio_transcriber/
├── main.py              # Ana uygulama & UI
├── audio_recorder.py    # Ses kayıt modülü
├── gladia_service.py    # Gladia API entegrasyonu
├── gemini_service.py    # Gemini AI entegrasyonu
├── config.py            # Konfigürasyon
├── requirements.txt     # Bağımlılıklar
├── .env.example         # Environment variables örneği
├── .gitignore           # Git ignore kuralları
└── recordings/          # Kayıt dosyaları (otomatik oluşur)
```

## 🎨 Arayüz Özellikleri

### Blok Kartları
- **▶️ Oynat/⏸️ Duraklat** - Blokları dinle
- **Progress Bar** - Oynatma ilerlemesi
- **Süre Göstergesi** - Her bloğun uzunluğu
- **Seçim Toggle** - Checkbox ile seçim
- **🗑️ Silme** - İstenmeyen blokları sil
- **Durum Göstergesi** - Çevriliyor... / ✓ Tamamlandı / ✗ Hata

### Toplu İşlemler
- **Tümü** - Tüm blokları seç
- **Hiçbiri** - Seçimi kaldır
- **Seçili Sayısı** - Kaç blok seçili gösterimi

## 🔧 Sorun Giderme

### "Mikrofon bulunamadı" hatası
- Windows Ses Ayarları'ndan varsayılan mikrofonu kontrol et
- Mikrofon iznini kontrol et

### "Loopback bulunamadı" hatası
- Windows'ta "Stereo Mix" veya "Stereo Karışımı" etkinleştir:
  - Ses Ayarları → Kayıt → Sağ tık → Devre Dışı Cihazları Göster
  - Stereo Mix/Karışımı'nı etkinleştir

### Gladia API hatası
- API key'i kontrol et
- İnternet bağlantısını kontrol et
- Gladia dashboard'dan kredi durumunu kontrol et

### Gemini API hatası
- API key'i kontrol et
- Günlük limit aşıldı mı kontrol et

## 🎯 Gelecek Özellikler

- [ ] Real-time transkripsiyon
- [ ] Konuşmacı ayrımı (diarization)
- [ ] Farklı not şablonları seçimi
- [ ] Otomatik dil algılama
- [ ] Ses kalitesi göstergesi
- [ ] Hotkey desteği
- [ ] Çoklu dil desteği
- [ ] Export formatları (PDF, DOCX)

## 🤝 Katkıda Bulunma

Pull request'ler memnuniyetle karşılanır. Büyük değişiklikler için lütfen önce bir issue açın.

## 📄 Lisans

MIT License

## 🙏 Teşekkürler

- [Gladia](https://gladia.io/) - Transkripsiyon API
- [Google Gemini](https://ai.google.dev/) - AI not çıkarma
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
