import speech_recognition as sr
from gtts import gTTS
import os
import time
import threading
import queue
import pygame
import tempfile

class SpeechSystem:
    def __init__(self):
        # Pygame mixer'ı başlat
        pygame.mixer.init()
        
        # Ses dosyaları için klasör oluştur
        self.SOUND_DIR = "temp_sounds"
        if not os.path.exists(self.SOUND_DIR):
            os.makedirs(self.SOUND_DIR)
        
        # Ses çalma kuyruğu
        self.sound_queue = queue.Queue()
        self.is_playing = False
        self.is_paused = False
        self.current_speed = 1.0  # Normal hız
        
        # Ses çalma thread'ini başlat
        self.playback_thread = threading.Thread(target=self._playback_worker, daemon=True)
        self.playback_thread.start()
    
    def _playback_worker(self):
        """Ses çalma kuyruğunu işleyen worker thread"""
        while True:
            try:
                sound_file = self.sound_queue.get()
                if sound_file:
                    self.is_playing = True
                    self.is_paused = False
                    # Pygame ile sesi çal
                    pygame.mixer.music.load(sound_file)
                    pygame.mixer.music.play()
                    # Ses bitene kadar bekle
                    while pygame.mixer.music.get_busy() and not self.is_paused:
                        pygame.time.Clock().tick(10)
                    self.is_playing = False
                    # Dosyayı temizle
                    try:
                        os.remove(sound_file)
                    except:
                        pass
                self.sound_queue.task_done()
            except Exception as e:
                print(f"Ses çalma hatası: {str(e)}")
                self.is_playing = False
                self.is_paused = False
    
    def stop_speech(self):
        """Sesi durdur"""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            return True
        return False
    
    def pause_speech(self):
        """Sesi duraklat"""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            return True
        return False
    
    def resume_speech(self):
        """Duraklatılmış sesi devam ettir"""
        if self.is_playing and self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            return True
        return False
    
    def set_speech_speed(self, speed):
        """Ses hızını ayarla (0.5 - 2.0 arası)"""
        try:
            speed = float(speed)
            if 0.5 <= speed <= 2.0:
                self.current_speed = speed
                return True
        except:
            pass
        return False
    
    def dinle_turkce(self):
        """Türkçe konuşmayı mikrofondan algılar"""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Lütfen konuşun...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                try:
                    metin = r.recognize_google(audio, language='tr-TR')
                    print(f"Algılanan metin: {metin}")
                    return metin
                except sr.UnknownValueError:
                    print("Sizi anlayamadım.")
                    return None
                except sr.RequestError as e:
                    print(f"Servise ulaşılamadı: {e}")
                    return None
            except sr.WaitTimeoutError:
                print("Dinleme zaman aşımına uğradı.")
                return None
            except Exception as e:
                print(f"Beklenmeyen hata: {str(e)}")
                return None
    
    def seslendir_turkce(self, metin):
        """Metni Türkçe olarak seslendirir"""
        try:
            # Geçici dosya oluştur
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3', dir=self.SOUND_DIR) as fp:
                temp_filename = fp.name
            
            # Metni sese çevir
            tts = gTTS(text=metin, lang='tr', slow=False)
            tts.save(temp_filename)
            
            # Sesi kuyruğa ekle
            self.sound_queue.put(temp_filename)
            
        except Exception as e:
            print(f"Seslendirme hatası: {str(e)}")
            return False
        return True

# Global speech system instance
speech_system = SpeechSystem()

def dinle_turkce():
    """Global dinleme fonksiyonu"""
    return speech_system.dinle_turkce()

def seslendir_turkce(metin):
    """Global seslendirme fonksiyonu"""
    return speech_system.seslendir_turkce(metin)

def stop_speech():
    """Global ses durdurma fonksiyonu"""
    return speech_system.stop_speech()

def pause_speech():
    """Global ses duraklatma fonksiyonu"""
    return speech_system.pause_speech()

def resume_speech():
    """Global ses devam ettirme fonksiyonu"""
    return speech_system.resume_speech()

def set_speech_speed(speed):
    """Global ses hızı ayarlama fonksiyonu"""
    return speech_system.set_speech_speed(speed)

# Test amaçlı ana fonksiyon
if __name__ == "__main__":
    komut = dinle_turkce()
    if komut:
        yanit = f"Şunu söylediniz: {komut}"
        seslendir_turkce(yanit)