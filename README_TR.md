# 🎙️ Audio Transcriber

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**[English](./README.md)** | **[Türkçe](#)**

Windows için profesyonel ses kayıt ve transkripsiyon uygulaması. Mikrofon ve sistem sesini aynı anda kaydedin, otomatik 10 dakikalık bloklara ayırın, Gladia AI ile transkript edin ve Gemini ile akıllı notlar oluşturun.

## ✨ Özellikler

- 🎤 **Çoklu Ses Kaydı** - Mikrofon ve sistem sesini aynı anda kaydet
- 📦 **Akıllı Blok Yönetimi** - Maliyet optimizasyonu için otomatik 10 dk'lık bloklar
- 🎮 **Oynatma Önizleme** - Çevirmeden önce her bloğu dinle
- ✅ **Esnek Seçim** - Hangi blokları çevireceğini seç
- 📝 **Gladia Transkripsiyon** - Yüksek doğruluklu Türkçe çeviri
- 🤖 **Gemini AI Notları** - Otomatik not oluşturma ve özetleme
- 💾 **Markdown Dışa Aktarma** - Notları kolayca kaydet ve paylaş
- 🎨 **Modern Arayüz** - CustomTkinter ile profesyonel arayüz
- 🗑️ **Blok Yönetimi** - İstenmeyen blokları sil
- 📊 **Toplu İşlemler** - Tek tıkla tümünü seç/kaldır
- ⏱️ **İlerleme Takibi** - Gerçek zamanlı kayıt ve oynatma ilerlemesi

## 📸 Ekran Görüntüleri

> *Yakında eklenecek - Arayüz ekran görüntüleri*

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.10 veya üzeri
- Windows işletim sistemi (sistem sesi kaydı için)
- [Gladia API Anahtarı](https://app.gladia.io/)
- [Gemini API Anahtarı](https://aistudio.google.com/apikey)

### Kurulum

1. **Depoyu klonlayın**
   ```bash
   git clone https://github.com/yourusername/audio_transcriber.git
   cd audio_transcriber
   ```

2. **Virtual environment oluşturun**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Bağımlılıkları yükleyin**
   ```bash
   pip install -r requirements.txt
   ```

4. **API anahtarlarını yapılandırın**

   `.env.example` dosyasını `.env` olarak kopyalayın:
   ```bash
   cp .env.example .env
   ```

   `.env` dosyasını düzenleyin ve API anahtarlarınızı ekleyin:
   ```env
   GLADIA_API_KEY=gladia-anahtarınız-buraya
   GEMINI_API_KEY=gemini-anahtarınız-buraya
   ```

5. **Uygulamayı çalıştırın**
   ```bash
   python main.py
   ```

## 📖 Kullanım

### Temel İş Akışı

1. **Ses Kaynaklarını Seçin**
   - Açılır menüden mikrofonu seçin
   - Gerekirse sistem sesini seçin (Stereo Mix/MOTIV Mix)

2. **Ses Kaydedin**
   - ⏺️ "Kayda Başla" butonuna tıklayın
   - Kayıt otomatik olarak 10 dakikalık bloklara bölünür
   - İşiniz bittiğinde ⏹️ "Durdur"a tıklayın

3. **Blokları Önizleyin**
   - Herhangi bir blok kartındaki ▶️ butonuna tıklayarak dinleyin
   - İlerleme çubuğu oynatma durumunu gösterir
   - Duraklatmak için ⏸️ tıklayın

4. **Blokları Seçin**
   - Transkripsiyon için blokları onay kutularıyla seçin
   - "Tümü" butonu tüm blokları seçer
   - "Hiçbiri" butonu seçimi kaldırır

5. **Transkript Edin**
   - "Seçilenleri Çevir →" butonuna tıklayın
   - Her blok için ilerlemeyi izleyin
   - Transkripti sağ panelde görüntüleyin

6. **Not Oluşturun**
   - 🤖 "Gemini ile Not Çıkar" butonuna tıklayın
   - AI transkripti analiz eder ve yapılandırılmış notlar oluşturur
   - Notlar alt panelde görünür

7. **Dışa Aktarın**
   - 💾 "Markdown Olarak Kaydet" butonuna tıklayın
   - Konum ve dosya adını seçin
   - Notlarınızı paylaşın!

### Sistem Sesini Etkinleştirme (Windows)

Sistem sesini kaydetmek için "Stereo Mix"i etkinleştirin:

1. Hoparlör simgesine sağ tıklayın → **Ses Ayarları**
2. **Ses Kontrol Paneli** → **Kayıt** sekmesine tıklayın
3. Boş alana sağ tıklayın → **Devre Dışı Cihazları Göster**
4. **Stereo Mix** veya **Stereo Karışımı**'na sağ tıklayın → **Etkinleştir**
5. Varsayılan olarak ayarlayın veya uygulamada seçin

## ⚙️ Yapılandırma

### Ortam Değişkenleri

| Değişken | Açıklama | Gerekli |
|----------|----------|---------|
| `GLADIA_API_KEY` | Gladia.io'dan API anahtarı | Evet |
| `GEMINI_API_KEY` | Google AI Studio'dan API anahtarı | Evet |

### Ayarlar (config.py)

| Ayar | Varsayılan | Açıklama |
|------|-----------|----------|
| `SAMPLE_RATE` | 44100 | Hz cinsinden ses örnekleme hızı |
| `BLOCK_DURATION_MINUTES` | 10 | Kayıt bloğu süresi |
| `RECORDINGS_DIR` | "recordings" | Ses dosyaları dizini |
| `GEMINI_MODEL` | "gemini-2.5-flash" | Gemini model sürümü |

## 💰 Maliyet Tahmini

| Servis | Birim Fiyat | 10 dk | 1 saat |
|--------|-------------|-------|--------|
| Gladia | ~$0.0002/sn | ~$0.12 | ~$0.70 |
| Gemini Flash | Ücretsiz* | $0 | $0 |

*Gemini 2.5 Flash günlük limitler içinde ücretsizdir.

## 📁 Proje Yapısı

```
audio_transcriber/
├── src/                 # Kaynak kod
│   ├── __init__.py
│   ├── audio_recorder.py    # Ses kayıt modülü
│   ├── gladia_service.py    # Gladia API entegrasyonu
│   ├── gemini_service.py    # Gemini AI entegrasyonu
│   └── config.py            # Yapılandırma
├── main.py              # Ana uygulama giriş noktası
├── recordings/          # Ses dosyaları (otomatik oluşur)
├── requirements.txt     # Bağımlılıklar
├── .env.example         # Ortam değişkenleri şablonu
├── .gitignore           # Git ignore kuralları
├── LICENSE              # MIT Lisansı
├── README.md            # İngilizce dokümantasyon
└── README_TR.md         # Türkçe dokümantasyon
```

## 🔧 Sorun Giderme

### "Mikrofon bulunamadı" hatası
- Windows Ses Ayarları'ndan varsayılan mikrofonu kontrol edin
- Uygulama için mikrofon izinlerini doğrulayın

### "Loopback bulunamadı" hatası
- Windows'ta "Stereo Mix" veya "Stereo Karışımı"'nı etkinleştirin:
  - Ses Ayarları → Kayıt → Sağ tık → Devre Dışı Cihazları Göster
  - Stereo Mix/Karışımı'nı etkinleştir

### Gladia API hataları
- API anahtarının doğru olduğunu kontrol edin
- İnternet bağlantınızı kontrol edin
- Gladia panelinden kredi bakiyesini kontrol edin

### Gemini API hataları
- API anahtarının doğru olduğunu kontrol edin
- Günlük limitin aşılıp aşılmadığını kontrol edin
- Model adının doğru olduğundan emin olun

## 🎯 Yol Haritası

- [ ] Gerçek zamanlı transkripsiyon
- [ ] Konuşmacı ayrımı (farklı konuşmacıları tanımlama)
- [ ] Çoklu not şablonları
- [ ] Otomatik dil algılama
- [ ] Ses kalitesi göstergesi
- [ ] Klavye kısayolları/hotkey'ler
- [ ] Çoklu dil desteği
- [ ] PDF ve DOCX'e aktarma
- [ ] Bulut depolama entegrasyonu
- [ ] İşbirliği özellikleri

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen bir Pull Request göndermekten çekinmeyin.

1. Projeyi fork edin
2. Özellik dalınızı oluşturun (`git checkout -b feature/HarikaOzellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Harika bir özellik ekle'`)
4. Dalınıza push edin (`git push origin feature/HarikaOzellik`)
5. Bir Pull Request açın

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [Gladia](https://gladia.io/) - Transkripsiyon API'si
- [Google Gemini](https://ai.google.dev/) - AI not oluşturma
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern UI framework
- [sounddevice](https://python-sounddevice.readthedocs.io/) - Ses I/O kütüphanesi
- [soundfile](https://github.com/bastibe/python-soundfile) - Ses dosyası işlemleri

## 📧 İletişim

Yunus Emre Alpak - [@yunusemrealpak](https://github.com/yunusemrealpak)

Proje Linki: [https://github.com/yourusername/audio_transcriber](https://github.com/yourusername/audio_transcriber)

---

<div align="center">
❤️ ile yapıldı - Yunus Emre Alpak
</div>
