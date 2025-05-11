import os
from dotenv import load_dotenv
import requests
import json
import webbrowser
from datetime import datetime
import locale

# .env dosyasını yükle
load_dotenv()

# API anahtarlarını .env dosyasından al
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

class APIServices:
    def __init__(self):
        self.weather_api_key = WEATHER_API_KEY
        self.news_api_key = NEWS_API_KEY
        self.spoonacular_api_key = "  "
        self.deepseek_api_key = DEEPSEEK_API_KEY
        
        # Türkçe tarih formatı için locale ayarı
        try:
            locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, 'tr_TR')
            except:
                pass

    def get_date_time(self):
        """Güncel tarih ve saat bilgisini getirir"""
        try:
            now = datetime.now()
            
            # Tarih formatı
            date_str = now.strftime("%d %B %Y")
            day_name = now.strftime("%A")
            
            # Saat formatı
            time_str = now.strftime("%H:%M")
            
            # Ay isimlerini Türkçeleştir
            months = {
                "January": "Ocak",
                "February": "Şubat",
                "March": "Mart",
                "April": "Nisan",
                "May": "Mayıs",
                "June": "Haziran",
                "July": "Temmuz",
                "August": "Ağustos",
                "September": "Eylül",
                "October": "Ekim",
                "November": "Kasım",
                "December": "Aralık"
            }
            
            # Gün isimlerini Türkçeleştir
            days = {
                "Monday": "Pazartesi",
                "Tuesday": "Salı",
                "Wednesday": "Çarşamba",
                "Thursday": "Perşembe",
                "Friday": "Cuma",
                "Saturday": "Cumartesi",
                "Sunday": "Pazar"
            }
            
            # Tarihi Türkçeleştir
            for eng, tr in months.items():
                date_str = date_str.replace(eng, tr)
            
            # Günü Türkçeleştir
            day_name = days.get(day_name, day_name)
            
            return f"Bugünün tarihi {date_str} {day_name}. Saat {time_str}."
            
        except Exception as e:
            print(f"Tarih/saat hatası: {str(e)}")
            return "Tarih ve saat bilgisi alınamadı."

    def get_weather(self, city):
        """Hava durumu bilgisini getirir"""
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric&lang=tr"
            
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]
                feels_like = data["main"]["feels_like"]
                
                # Hava durumu açıklamalarını Türkçeleştir
                weather_descriptions = {
                    "clear sky": "Açık",
                    "few clouds": "Az Bulutlu",
                    "scattered clouds": "Parçalı Bulutlu",
                    "broken clouds": "Çok Bulutlu",
                    "shower rain": "Sağanak Yağışlı",
                    "rain": "Yağmurlu",
                    "thunderstorm": "Gök Gürültülü Fırtına",
                    "snow": "Karlı",
                    "mist": "Sisli",
                    "overcast clouds": "Kapalı",
                    "light rain": "Hafif Yağmurlu",
                    "moderate rain": "Orta Şiddetli Yağmur",
                    "heavy intensity rain": "Şiddetli Yağmur",
                    "very heavy rain": "Çok Şiddetli Yağmur",
                    "extreme rain": "Aşırı Yağmur",
                    "freezing rain": "Dondurucu Yağmur",
                    "light intensity drizzle": "Hafif Çisenti",
                    "drizzle": "Çisenti",
                    "heavy intensity drizzle": "Şiddetli Çisenti",
                    "light intensity shower rain": "Hafif Sağanak",
                    "shower rain": "Sağanak",
                    "heavy intensity shower rain": "Şiddetli Sağanak",
                    "ragged shower rain": "Düzensiz Sağanak",
                    "light snow": "Hafif Kar",
                    "snow": "Kar",
                    "heavy snow": "Yoğun Kar",
                    "sleet": "Karla Karışık Yağmur",
                    "shower sleet": "Karla Karışık Sağanak",
                    "light rain and snow": "Hafif Yağmur ve Kar",
                    "rain and snow": "Yağmur ve Kar",
                    "light shower snow": "Hafif Kar Sağanağı",
                    "shower snow": "Kar Sağanağı",
                    "heavy shower snow": "Yoğun Kar Sağanağı",
                    "smoke": "Dumanlı",
                    "haze": "Puslu",
                    "sand/dust whirls": "Kum/Toz Fırtınası",
                    "fog": "Sisli",
                    "sand": "Kumlu",
                    "dust": "Tozlu",
                    "volcanic ash": "Volkanik Kül",
                    "squalls": "Sert Rüzgarlı",
                    "tornado": "Kasırga",
                    "tropical storm": "Tropik Fırtına",
                    "hurricane": "Kasırga",
                    "cold": "Soğuk",
                    "hot": "Sıcak",
                    "windy": "Rüzgarlı",
                    "hail": "Dolu"
                }
                
                # Açıklamayı Türkçeleştir
                desc = weather_descriptions.get(desc.lower(), desc)
                
                return (
                    f"{city} için hava durumu bilgisi:\n"
                    f"• Sıcaklık: {temp:.1f}°C\n"
                    f"• Hissedilen: {feels_like:.1f}°C\n"
                    f"• Durum: {desc}\n"
                    f"• Nem: %{humidity}\n"
                    f"• Rüzgar: {wind} m/s"
                )
            else:
                return f"Üzgünüm, {city} için hava durumu bilgisi alınamadı."
                
        except Exception as e:
            print(f"Hava durumu hatası: {str(e)}")
            return "Hava durumu bilgisi alınırken bir hata oluştu."

    def get_news(self):
        """Güncel haberleri getirir"""
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=tr&apiKey={self.news_api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data["status"] == "ok":
                articles = data["articles"][:5]  # İlk 5 haberi al
                news_text = "📰 Güncel Haberler:\n\n"
                
                for i, article in enumerate(articles, 1):
                    title = article["title"]
                    source = article["source"]["name"]
                    news_text += f"{i}. {title}\n   Kaynak: {source}\n\n"
                
                return news_text
            else:
                return "Üzgünüm, haberler alınamadı. Lütfen daha sonra tekrar deneyin."
                
        except Exception as e:
            print(f"Haber hatası: {str(e)}")
            return "Haberler alınırken bir hata oluştu."

    def get_sports_news(self):
        """Spor haberlerini getirir"""
        try:
            url = f"https://newsapi.org/v2/everything?q=spor&language=tr&sortBy=publishedAt&apiKey={self.news_api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data["status"] == "ok":
                articles = data["articles"][:5]  # İlk 5 haberi al
                news_text = "⚽ Spor Haberleri:\n\n"
                
                for i, article in enumerate(articles, 1):
                    title = article["title"]
                    source = article["source"]["name"]
                    news_text += f"{i}. {title}\n   Kaynak: {source}\n\n"
                
                return news_text
            else:
                return "Üzgünüm, spor haberleri alınamadı. Lütfen daha sonra tekrar deneyin."
                
        except Exception as e:
            print(f"Spor haberleri hatası: {str(e)}")
            return "Spor haberleri alınırken bir hata oluştu."

    def process_news_request(self, query):
        """Haber isteğini işler"""
        query = query.lower().strip()
        
        if "spor" in query:
            return self.get_sports_news()
        elif "ekonomi" in query:
            url = f"https://newsapi.org/v2/everything?q=ekonomi&language=tr&sortBy=publishedAt&apiKey={self.news_api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data["status"] == "ok":
                articles = data["articles"][:5]
                news_text = "💰 Ekonomi Haberleri:\n\n"
                
                for i, article in enumerate(articles, 1):
                    title = article["title"]
                    source = article["source"]["name"]
                    news_text += f"{i}. {title}\n   Kaynak: {source}\n\n"
                
                return news_text
            else:
                return "Üzgünüm, ekonomi haberleri alınamadı."
                
        elif "teknoloji" in query:
            url = f"https://newsapi.org/v2/everything?q=teknoloji&language=tr&sortBy=publishedAt&apiKey={self.news_api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data["status"] == "ok":
                articles = data["articles"][:5]
                news_text = "💻 Teknoloji Haberleri:\n\n"
                
                for i, article in enumerate(articles, 1):
                    title = article["title"]
                    source = article["source"]["name"]
                    news_text += f"{i}. {title}\n   Kaynak: {source}\n\n"
                
                return news_text
            else:
                return "Üzgünüm, teknoloji haberleri alınamadı."
                
        elif "kültür" in query or "sanat" in query:
            url = f"https://newsapi.org/v2/everything?q=kültür+sanat&language=tr&sortBy=publishedAt&apiKey={self.news_api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200 and data["status"] == "ok":
                articles = data["articles"][:5]
                news_text = "🎭 Kültür-Sanat Haberleri:\n\n"
                
                for i, article in enumerate(articles, 1):
                    title = article["title"]
                    source = article["source"]["name"]
                    news_text += f"{i}. {title}\n   Kaynak: {source}\n\n"
                
                return news_text
            else:
                return "Üzgünüm, kültür-sanat haberleri alınamadı."
        else:
            return self.get_news()

    def get_recipe(self):
        """Rastgele yemek tarifi önerir"""
        try:
            # Spoonacular API'den rastgele tarif al
            url = f"https://api.spoonacular.com/recipes/random?apiKey={self.spoonacular_api_key}&number=1&tags=turkish&addRecipeInformation=true"
            response = requests.get(url)
            
            # API yanıtını kontrol et
            if response.status_code == 200:
                data = response.json()
                if "recipes" in data and len(data["recipes"]) > 0:
                    recipe = data["recipes"][0]
                    
                    # Tarif bilgilerini al
                    title = recipe.get("title", "İsimsiz Tarif")
                    ingredients = recipe.get("extendedIngredients", [])
                    instructions = recipe.get("instructions", "Tarif talimatları bulunamadı.")
                    prep_time = recipe.get("readyInMinutes", "Bilinmiyor")
                    servings = recipe.get("servings", "Bilinmiyor")
                    
                    # Malzemeleri formatla
                    ingredients_text = "Malzemeler:\n"
                    for ingredient in ingredients:
                        amount = ingredient.get("amount", "")
                        unit = ingredient.get("unit", "")
                        name = ingredient.get("name", "")
                        if amount and unit and name:
                            ingredients_text += f"• {amount} {unit} {name}\n"
                    
                    # Talimatları formatla
                    instructions_text = "\nHazırlanışı:\n" + instructions
                    
                    return (
                        f"🍽️ Önerilen Tarif: {title}\n\n"
                        f"⏱️ Hazırlama Süresi: {prep_time} dakika\n"
                        f"👥 Porsiyon: {servings} kişilik\n\n"
                        f"{ingredients_text}\n"
                        f"{instructions_text}"
                    )
                else:
                    print("API yanıtında tarif bulunamadı")
                    return self.get_sample_recipe()
            else:
                print(f"API Hatası - Durum Kodu: {response.status_code}")
                print(f"API Yanıtı: {response.text}")
                return self.get_sample_recipe()
                
        except Exception as e:
            print(f"Tarif hatası: {str(e)}")
            return self.get_sample_recipe()
            
    def get_sample_recipe(self):
        """Örnek bir Türk yemek tarifi döndürür"""
        return (
            "🍽️ Önerilen Tarif: Mercimek Çorbası\n\n"
            "⏱️ Hazırlama Süresi: 30 dakika\n"
            "👥 Porsiyon: 4 kişilik\n\n"
            "Malzemeler:\n"
            "• 1 su bardağı kırmızı mercimek\n"
            "• 1 adet soğan\n"
            "• 1 adet havuç\n"
            "• 1 adet patates\n"
            "• 2 yemek kaşığı un\n"
            "• 1 yemek kaşığı tereyağı\n"
            "• 1 tatlı kaşığı tuz\n"
            "• 1/2 çay kaşığı karabiber\n"
            "• 1/2 çay kaşığı pul biber\n"
            "• 6 su bardağı su\n\n"
            "Hazırlanışı:\n"
            "1. Mercimekleri yıkayın ve süzün.\n"
            "2. Soğanı, havucu ve patatesi küp küp doğrayın.\n"
            "3. Tereyağını tencerede eritin.\n"
            "4. Soğanları ekleyip yumuşayana kadar kavurun.\n"
            "5. Havuç ve patatesleri ekleyip 2-3 dakika daha kavurun.\n"
            "6. Unu ekleyip 1 dakika daha kavurun.\n"
            "7. Mercimekleri ekleyin ve karıştırın.\n"
            "8. Suyu ekleyin ve kaynamaya bırakın.\n"
            "9. Sebzeler yumuşayınca blenderdan geçirin.\n"
            "10. Tuz ve baharatları ekleyip 5 dakika daha pişirin.\n"
            "11. Sıcak servis yapın.\n\n"
            "Afiyet olsun! 😊"
        )

    def open_youtube(self):
        """YouTube'u açar"""
        try:
            webbrowser.open("https://www.youtube.com")
            return "YouTube açılıyor..."
        except Exception as e:
            return f"YouTube açılamadı: {str(e)}"

    def chat_with_deepseek(self, message):
        """DeepSeek AI ile sohbet eder"""
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Alfa Asistan"
            }
            
            data = {
                "model": "deepseek/deepseek-chat:free",
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    return "Üzgünüm, bir yanıt alınamadı."
            else:
                print(f"DeepSeek API Hatası - Durum Kodu: {response.status_code}")
                print(f"API Yanıtı: {response.text}")
                return "Üzgünüm, şu anda yanıt veremiyorum. Lütfen daha sonra tekrar deneyin."
                
        except Exception as e:
            print(f"DeepSeek sohbet hatası: {str(e)}")
            return "Sohbet sırasında bir hata oluştu. Lütfen daha sonra tekrar deneyin." 