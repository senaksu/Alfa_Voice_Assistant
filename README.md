# 🎙️ Alfa -  Sesli Asistan

Alfa, Python ile geliştirilmiş, modern ve kullanıcı dostu bir Türkçe sesli asistan uygulamasıdır. Kullanıcılar sesli komutlar veya metin girişi ile asistanla etkileşime geçebilir.

## 🌟 Özellikler

- 🎤 Sesli komut desteği
- 🌤️ Hava durumu bilgisi
- 📰 Güncel haberler
- 🍳 Yemek tarifleri
- 🔍 Web araması
- 📺 YouTube video araması
- 🎵 Müzik çalma
- 📝 Not alma
- 🎨 Özelleştirilebilir arayüz
- 🌙 Karanlık/Aydınlık tema desteği

## 🚀 Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/senaksu/Alfa_voice_assistant
cd alfa-asistan
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. `.env` dosyasını oluşturun ve API anahtarlarınızı ekleyin:
```env
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
NEWS_API_KEY=your_news_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

4. Uygulamayı başlatın:
```bash
python main.py
```

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- PyQt6
- SpeechRecognition
- gTTS
- requests
- python-dotenv
- diğer gerekli paketler (requirements.txt dosyasında listelenmiştir)

## 🎯 Kullanım

1. **Sesli Komutlar:**
   - Mikrofon butonuna basılı tutarak konuşun
   - Komutunuzu tamamladıktan sonra butonu bırakın

2. **Metin Girişi:**
   - Alt kısımdaki metin kutusuna komutunuzu yazın
   - Gönder butonuna tıklayın veya Enter tuşuna basın

3. **Örnek Komutlar:**
   - "İstanbul hava durumu"
   - "Güncel haberler"
   - "Bana bir yemek tarifi öner"
   - "YouTube'da kedi videoları ara"
   - "Not al: Yarın toplantı var"

## 🛠️ API Anahtarları

Uygulamanın çalışması için aşağıdaki API anahtarlarına ihtiyaç vardır:

1. **OpenAI API Key:**
   - https://platform.openai.com adresinden alabilirsiniz
   - Ücretsiz deneme sürümü mevcuttur

2. **Weather API Key:**
   - https://openweathermap.org adresinden alabilirsiniz
   - Ücretsiz plan mevcuttur

3. **News API Key:**
   - https://newsapi.org adresinden alabilirsiniz
   - Ücretsiz plan mevcuttur

4. **DeepSeek API Key:**
   - https://deepseek.com adresinden alabilirsiniz
   - Ücretsiz deneme sürümü mevcuttur



## 👥 İletişim

- GitHub: [@senaksu](https://github.com/senaksu)


