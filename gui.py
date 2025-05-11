import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from speech import dinle_turkce, seslendir_turkce, stop_speech, pause_speech, resume_speech, set_speech_speed
import webbrowser
from datetime import datetime
from api_services import APIServices
import time

class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=200, height=40, corner_radius=10, bg="#2d5bb9", fg="white", hover_color="#3a6bc7", **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"], highlightthickness=0, **kwargs)
        self.command = command
        self.bg = bg
        self.hover_color = hover_color
        self.fg = fg
        
        # Yuvarlak köşeli dikdörtgen çiz
        self.rect = self.create_rounded_rect(0, 0, width, height, corner_radius, fill=bg)
        self.text = self.create_text(width/2, height/2, text=text, fill=fg, font=("Helvetica", 12))
        
        # Tıklama olayları
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def _on_click(self, event):
        if self.command:
            self.command()
            
    def _on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_color)
        
    def _on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg)

class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Alfa - Türkçe Sesli Asistan")
        self.root.geometry("1200x800")
        
        # API servisleri
        self.api = APIServices()
        
        # Tema ayarları
        self.is_dark_mode = True
        self.setup_theme()
        
        self.is_listening = False
        self.notes = []
        self.setup_gui()
        
        # Animasyon için değişkenler
        self.animation_running = False
        self.start_animation()
        
    def setup_theme(self):
        if self.is_dark_mode:
            self.bg_color = "#1a1a1a"
            self.text_color = "#ffffff"
            self.button_color = "#2d5bb9"
            self.message_bg = "#2d5bb9"
            self.user_message_bg = "#2d2d2d"
            self.accent_color = "#4a90e2"
            self.hover_color = "#3a6bc7"
            self.secondary_bg = "#2d2d2d"
            self.border_color = "#3d3d3d"
            self.chat_bg = "#1e1e1e"
        else:
            self.bg_color = "#ffffff"
            self.text_color = "#000000"
            self.button_color = "#007bff"
            self.message_bg = "#007bff"
            self.user_message_bg = "#f0f0f0"
            self.accent_color = "#0056b3"
            self.hover_color = "#0056b3"
            self.secondary_bg = "#f8f9fa"
            self.border_color = "#dee2e6"
            self.chat_bg = "#f5f5f5"
            
    def setup_gui(self):
        # Ana container
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sol panel
        self.left_panel = tk.Frame(self.main_container, bg=self.bg_color, width=300)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        self.left_panel.pack_propagate(False)
        
        # Logo ve başlık
        self.setup_header()
        
        # Özellik butonları
        self.setup_feature_buttons()
        
        # Sağ panel
        self.right_panel = tk.Frame(self.main_container, bg=self.bg_color)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Sohbet alanı
        self.setup_chat_area()
        
        # Alt bar (Ses kontrolleri)
        self.setup_bottom_bar()
        
    def setup_header(self):
        header_frame = tk.Frame(self.left_panel, bg=self.bg_color, pady=30)
        header_frame.pack(fill=tk.X)
        
        # Logo animasyonu için canvas
        self.logo_canvas = tk.Canvas(header_frame, width=100, height=100, 
                                   bg=self.bg_color, highlightthickness=0)
        self.logo_canvas.pack(pady=(0, 15))
        
        # Logo çizimi
        self.draw_logo()
        
        title_label = tk.Label(header_frame, text="Alfa", font=("Helvetica", 36, "bold"),
                             bg=self.bg_color, fg=self.accent_color)
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(header_frame, text="Türkçe Sesli Asistan",
                                font=("Helvetica", 14), bg=self.bg_color, fg=self.text_color)
        subtitle_label.pack()
        
    def draw_logo(self):
        # Logo çizimi
        self.logo_canvas.delete("all")
        size = 80
        x, y = 50, 50
        
        # Dış daire
        self.logo_canvas.create_oval(x-size/2, y-size/2, x+size/2, y+size/2,
                                   outline=self.accent_color, width=3)
        
        # İç daire
        self.logo_canvas.create_oval(x-size/3, y-size/3, x+size/3, y+size/3,
                                   outline=self.accent_color, width=2)
        
        # Merkez nokta
        self.logo_canvas.create_oval(x-5, y-5, x+5, y+5,
                                   fill=self.accent_color)
        
    def start_animation(self):
        """Logo animasyonunu başlatır"""
        if not self.animation_running:
            self.animation_running = True
            self.animate_logo()
            
    def animate_logo(self):
        """Logo animasyonunu gerçekleştirir"""
        if self.animation_running:
            self.draw_logo()
            self.root.after(100, self.animate_logo)
            
    def create_button(self, parent, text, command, icon=None):
        """Modern görünümlü buton oluşturur"""
        btn_frame = tk.Frame(parent, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, pady=5, padx=10)
        
        btn = RoundedButton(btn_frame, f"{icon} {text}" if icon else text,
                          command=command, width=280, height=45,
                          corner_radius=15, bg=self.button_color,
                          fg="#ffffff", hover_color=self.hover_color)
        btn.pack(fill=tk.X)
        
        return btn
        
    def setup_feature_buttons(self):
        features = [
            ("🌐 Web'de Ara", self.search_web, "web"),
            ("🎵 Müzik Aç", self.play_music, "music"),
            ("📝 Not Al", self.take_note, "note"),
            ("📋 Notlarım", self.show_notes, "notes"),
            ("🎥 YouTube'da Ara", self.search_youtube, "youtube"),
            ("🌓 Tema Değiştir", self.toggle_theme, "theme")
        ]
        
        for text, command, icon in features:
            self.create_button(self.left_panel, text, command, icon)
            
    def setup_chat_area(self):
        # Sohbet alanı container
        chat_container = tk.Frame(self.right_panel, bg=self.bg_color)
        chat_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Başlık ve temizleme butonu için üst frame
        header_frame = tk.Frame(chat_container, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Başlık
        chat_title = tk.Label(header_frame, text="Sohbet",
                            font=("Helvetica", 16, "bold"),
                            bg=self.bg_color, fg=self.accent_color)
        chat_title.pack(side=tk.LEFT)
        
        # Temizleme butonu
        clear_button = RoundedButton(header_frame, "🗑️ Temizle", self.clear_chat,
                                   width=120, height=35, corner_radius=15,
                                   bg=self.button_color, fg="#ffffff",
                                   hover_color=self.hover_color)
        clear_button.pack(side=tk.RIGHT)
        
        # Sohbet alanı
        self.chat_area = scrolledtext.ScrolledText(chat_container, wrap=tk.WORD,
                                                 font=("Helvetica", 13),
                                                 bg=self.chat_bg,
                                                 fg=self.text_color,
                                                 padx=15, pady=15)
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # Hoş geldin mesajı
        welcome_msg = (
            "👋 Merhaba! Ben Alfa, Türkçe sesli asistanınız.\n\n"
            "Size nasıl yardımcı olabilirim?\n"
            "• Hava durumu bilgisi alabilirim\n"
            "• Haberleri okuyabilirim\n"
            "• Yemek tarifi önerebilirim\n"
            "• Web'de arama yapabilirim\n"
            "• YouTube'da video arayabilirim\n"
            "• Müzik açabilirim\n"
            "• Not alabilirim\n\n"
            "Mikrofon butonuna tıklayarak veya sol menüden özellikleri kullanarak başlayabilirsiniz."
        )
        self.add_message(welcome_msg, False)
        
    def setup_bottom_bar(self):
        bottom_bar = tk.Frame(self.right_panel, bg=self.secondary_bg, pady=15)
        bottom_bar.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # Sol taraf - Mikrofon ve metin girişi
        left_frame = tk.Frame(bottom_bar, bg=self.secondary_bg)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15)
        
        # Mikrofon butonu
        self.mic_button = RoundedButton(left_frame, "🎤", self.toggle_listening,
                                      width=50, height=50, corner_radius=25,
                                      bg=self.button_color, fg="#ffffff",
                                      hover_color=self.hover_color)
        self.mic_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Mikrofon butonuna basılı tutma olaylarını ekle
        self.mic_button.bind("<ButtonPress-1>", lambda e: self.toggle_listening())
        self.mic_button.bind("<ButtonRelease-1>", lambda e: self.stop_listening())
        
        # Metin girişi ve gönder butonu container
        input_container = tk.Frame(left_frame, bg=self.secondary_bg)
        input_container.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Metin girişi
        input_frame = tk.Frame(input_container, bg=self.secondary_bg,
                             highlightbackground=self.border_color,
                             highlightthickness=1)
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.input_field = tk.Entry(input_frame, font=("Helvetica", 13),
                                  bg=self.secondary_bg, fg=self.text_color,
                                  bd=0, insertbackground=self.text_color)
        self.input_field.pack(fill=tk.X, padx=10, pady=8)
        self.input_field.bind("<Return>", lambda e: self.send_message())
        
        # Gönder butonu
        send_button = RoundedButton(input_container, "➤", lambda: self.send_message(),
                                  width=40, height=40, corner_radius=20,
                                  bg=self.button_color, fg="#ffffff",
                                  hover_color=self.hover_color)
        send_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Sağ taraf - Ses kontrolleri
        right_frame = tk.Frame(bottom_bar, bg=self.secondary_bg)
        right_frame.pack(side=tk.RIGHT, padx=15)
        
        # Ses kontrol butonları
        controls = [
            ("⏹️", stop_speech),
            ("⏸️", pause_speech),
            ("▶️", resume_speech)
        ]
        
        for icon, command in controls:
            btn = RoundedButton(right_frame, icon, command,
                              width=40, height=40, corner_radius=20,
                              bg=self.button_color, fg="#ffffff",
                              hover_color=self.hover_color)
            btn.pack(side=tk.LEFT, padx=5)
        
        # Hız kontrolü
        speed_frame = tk.Frame(right_frame, bg=self.secondary_bg)
        speed_frame.pack(side=tk.LEFT, padx=10)
        
        speed_label = tk.Label(speed_frame, text="Hız:", font=("Helvetica", 12),
                             bg=self.secondary_bg, fg=self.text_color)
        speed_label.pack(side=tk.LEFT, padx=5)
        
        self.speed_slider = ttk.Scale(speed_frame, from_=1, to=2,
                                    orient=tk.HORIZONTAL, length=100,
                                    command=self.update_speed)
        self.speed_slider.set(1)
        self.speed_slider.pack(side=tk.LEFT)
        
        self.speed_value_label = tk.Label(speed_frame, text="1x",
                                        font=("Helvetica", 12),
                                        bg=self.secondary_bg, fg=self.text_color,
                                        width=3)
        self.speed_value_label.pack(side=tk.LEFT, padx=5)
        
    def add_message(self, text, is_user=True):
        self.chat_area.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")
        
        if is_user:
            self.chat_area.insert(tk.END, f"\n[{timestamp}] 👤 Siz:\n", "user_header")
            self.chat_area.insert(tk.END, f"{text}\n", "user_message")
        else:
            self.chat_area.insert(tk.END, f"\n[{timestamp}] 🤖 Alfa:\n", "assistant_header")
            self.chat_area.insert(tk.END, f"{text}\n", "assistant_message")
            
        self.chat_area.tag_configure("user_header", font=("Helvetica", 13, "bold"),
                                   foreground=self.text_color)
        self.chat_area.tag_configure("user_message", font=("Helvetica", 13),
                                   foreground=self.text_color)
        self.chat_area.tag_configure("assistant_header", font=("Helvetica", 13, "bold"),
                                   foreground=self.accent_color)
        self.chat_area.tag_configure("assistant_message", font=("Helvetica", 13),
                                   foreground=self.text_color)
        
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)
        
    def update_widget_colors(self):
        """Tema değişikliğinde tüm widget renklerini günceller"""
        # Ana container renkleri
        self.root.configure(bg=self.bg_color)
        self.main_container.configure(bg=self.bg_color)
        self.left_panel.configure(bg=self.bg_color)
        self.right_panel.configure(bg=self.bg_color)
        
        # Sohbet alanı renkleri
        self.chat_area.configure(bg=self.chat_bg, fg=self.text_color)
        
        # Metin girişi renkleri
        self.input_field.configure(bg=self.secondary_bg, fg=self.text_color,
                                 insertbackground=self.text_color)
        
        # Hız kontrolü renkleri
        if hasattr(self, 'speed_value_label'):
            self.speed_value_label.configure(bg=self.secondary_bg, fg=self.text_color)
        
        # Tüm etiketleri güncelle
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label):
                widget.configure(bg=self.bg_color, fg=self.text_color)
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=self.bg_color)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=self.bg_color, fg=self.text_color)
                    elif isinstance(child, tk.Frame):
                        child.configure(bg=self.bg_color)
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.configure(bg=self.bg_color, fg=self.text_color)
        
        # Sohbet alanındaki mesaj etiketlerini güncelle
        self.chat_area.tag_configure("user_header", font=("Helvetica", 13, "bold"),
                                   foreground=self.text_color)
        self.chat_area.tag_configure("user_message", font=("Helvetica", 13),
                                   foreground=self.text_color)
        self.chat_area.tag_configure("assistant_header", font=("Helvetica", 13, "bold"),
                                   foreground=self.accent_color)
        self.chat_area.tag_configure("assistant_message", font=("Helvetica", 13),
                                   foreground=self.text_color)
        
        # Alt bar renkleri
        for widget in self.right_panel.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=self.secondary_bg)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        child.configure(bg=self.secondary_bg)
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, tk.Label):
                                grandchild.configure(bg=self.secondary_bg, fg=self.text_color)
                            elif isinstance(grandchild, tk.Frame):
                                grandchild.configure(bg=self.secondary_bg)
                                for great_grandchild in grandchild.winfo_children():
                                    if isinstance(great_grandchild, tk.Label):
                                        great_grandchild.configure(bg=self.secondary_bg,
                                                                fg=self.text_color)
        
    def toggle_theme(self):
        """Temayı değiştirir ve tüm renkleri günceller"""
        self.is_dark_mode = not self.is_dark_mode
        self.setup_theme()
        self.update_widget_colors()
        
        # Tema değişikliği mesajı
        theme_text = "Koyu tema" if self.is_dark_mode else "Açık tema"
        self.add_message(f"Tema {theme_text} olarak değiştirildi.", False)
        
    def toggle_listening(self):
        """Mikrofon butonuna basıldığında dinlemeyi başlatır"""
        self.is_listening = True
        self.mic_button.itemconfig(self.mic_button.rect, fill="#dc3545")
        self.mic_button.itemconfig(self.mic_button.text, text="🔴")
        self.add_message("Sizi dinliyorum...", False)
        threading.Thread(target=self.listen_once, daemon=True).start()

    def stop_listening(self):
        """Mikrofon butonu bırakıldığında dinlemeyi durdurur"""
        self.is_listening = False
        self.mic_button.itemconfig(self.mic_button.rect, fill=self.button_color)
        self.mic_button.itemconfig(self.mic_button.text, text="🎤")
        self.add_message("Dinleme durduruldu.", False)

    def listen_once(self):
        """Tek seferlik ses dinleme işlemi"""
        try:
            command = dinle_turkce()
            if command:
                # Asistanın kendi mesajlarını kontrol et
                if any(phrase in command.lower() for phrase in [
                    "🤖 alfa:", "alfa:", "merhaba! size nasıl yardımcı olabilirim",
                    "sizi dinliyorum", "dinleme durduruldu", "için hava durumu bilgisi",
                    "sıcaklık:", "hissedilen:", "durum:", "nem:", "rüzgar:"
                ]):
                    return

                # Kullanıcı mesajını ekle
                self.root.after(0, lambda: self.add_message(command, True))
                
                # Komutu işle ve yanıtı al
                response = self.process_command(command)
                
                # Yanıtı ekle ve seslendir
                if response:
                    self.root.after(0, lambda: self.add_message(response, False))
                    seslendir_turkce(response)
                    
        except Exception as e:
            print(f"Ses dinleme hatası: {str(e)}")
            self.root.after(0, lambda: self.add_message("Ses algılama sırasında bir hata oluştu.", False))

    def send_message(self, event=None):
        """Mesaj gönderme işlemini gerçekleştirir"""
        try:
            message = self.input_field.get().strip()
            if message:
                # Kullanıcı mesajını ekle
                self.add_message(message, True)
                
                # Komutu işle ve yanıtı al
                response = self.process_command(message)
                
                # Eğer yanıt None ise (asistanın kendi mesajı), işlemi sonlandır
                if response is None:
                    self.input_field.delete(0, tk.END)
                    return
                
                # Yanıtı ekle
                self.add_message(response, False)
                
                # Metin alanını temizle
                self.input_field.delete(0, tk.END)
                
                # Yanıtı seslendir
                seslendir_turkce(response)
                
        except Exception as e:
            print(f"Mesaj gönderme hatası: {str(e)}")
            self.add_message("Mesaj gönderilirken bir hata oluştu.", False)
            
    def update_speed(self, value):
        """Konuşma hızını günceller"""
        try:
            speed = int(float(value))
            if hasattr(self, 'speed_value_label'):
                self.speed_value_label.config(text=f"{speed}x")
            set_speech_speed(speed)
        except Exception as e:
            print(f"Hız güncelleme hatası: {str(e)}")
            
    def process_command(self, command):
        """Komutları işler ve uygun yanıtı döndürür"""
        try:
            if isinstance(command, str):
                command = command.lower().strip()
            else:
                return "Üzgünüm, bu komutu anlayamadım."
            
            # Asistanın kendi mesajlarını işleme
            if any(phrase in command.lower() for phrase in [
                "🤖 alfa:", "alfa:", "merhaba! size nasıl yardımcı olabilirim",
                "sizi dinliyorum", "dinleme durduruldu", "için hava durumu bilgisi",
                "sıcaklık:", "hissedilen:", "durum:", "nem:", "rüzgar:"
            ]):
                return None
            
            # Selamlama komutları
            if any(word in command for word in ["merhaba", "selam", "hey", "alo"]):
                return "Merhaba! Size nasıl yardımcı olabilirim?"
            
            # Tarih ve saat
            if any(word in command for word in ["saat", "tarih", "gün"]):
                return self.api.get_date_time()
            
            # Hava durumu komutları
            if "hava" in command or "hava durumu" in command:
                # Tüm gereksiz kelimeleri temizle
                city = command.replace("hava", "").replace("durumu", "").replace("için", "").strip()
                # Sayısal değerleri ve özel karakterleri temizle
                city = ''.join(c for c in city if not c.isdigit() and c not in '%°C')
                if not city:
                    return "Hangi şehir için hava durumu bilgisi istiyorsunuz?"
                return self.api.get_weather(city)
            
            # Haber komutları
            if "haber" in command:
                return self.api.process_news_request(command)
            
            # Yemek tarifi komutları
            if any(word in command for word in ["tarif", "yemek", "yemek tarifi"]):
                return self.api.get_recipe()
            
            # YouTube komutları
            if "youtube" in command:
                if "ara" in command:
                    query = command.replace("youtube", "").replace("ara", "").strip()
                    if not query:
                        return "YouTube'da ne aramak istediğinizi söyleyin."
                    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                    return f"YouTube'da '{query}' için arama yapılıyor..."
                else:
                    return self.api.open_youtube()
            
            # Müzik komutları
            if any(word in command for word in ["müzik", "şarkı", "çal"]):
                query = command.replace("müzik", "").replace("şarkı", "").replace("çal", "").strip()
                if not query:
                    return "Hangi müziği dinlemek istediğinizi söyleyin."
                webbrowser.open(f"https://www.youtube.com/results?search_query={query}+music")
                return f"'{query}' müziği aranıyor..."
            
            # Web arama komutları - Sadece "ara" kelimesi tek başına veya başta ise
            if command.startswith("ara ") or command == "ara":
                query = command.replace("ara", "").strip()
                if not query:
                    return "Ne aramak istediğinizi söyleyin."
                webbrowser.open(f"https://www.google.com/search?q={query}")
                return f"'{query}' için web araması yapılıyor..."
            
            # Not alma komutları
            if "not" in command:
                if "al" in command:
                    note = command.replace("not", "").replace("al", "").strip()
                    if not note:
                        self.add_message("Notunuzu söyleyin...", False)
                        seslendir_turkce("Notunuzu söyleyin...")
                        note = dinle_turkce()
                        if not note:
                            return "Not alınamadı. Lütfen tekrar deneyin."
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                    self.notes.append((timestamp, note))
                    return f"Not alındı: {note}"
                elif "notlarım" in command or "notları göster" in command:
                    if not self.notes:
                        return "Henüz not bulunmuyor."
                    notes_text = "📝 Notlarınız:\n\n"
                    for timestamp, note in self.notes:
                        notes_text += f"[{timestamp}]\n{note}\n\n"
                    return notes_text
            
            # Yardım komutu
            if "yardım" in command or "ne yapabilirsin" in command:
                return (
                    "Size şu konularda yardımcı olabilirim:\n"
                    "• Tarih ve saat bilgisi\n"
                    "• Hava durumu bilgisi\n"
                    "• Güncel haberler\n"
                    "• Yemek tarifleri\n"
                    "• YouTube'da video arama\n"
                    "• Müzik çalma\n"
                    "• Web'de arama yapma\n"
                    "• Not alma ve notları görüntüleme\n"
                    "• Tema değiştirme\n"
                    "• Sohbet etme\n\n"
                    "Ayrıca sol menüden özellikleri de kullanabilirsiniz."
                )
            
            # Eğer komut bir şehir adı ise, hava durumu sorgusu olarak işle
            if len(command.split()) == 1 and command not in ["ara", "yardım", "not"]:
                return self.api.get_weather(command)
            
            # Diğer tüm komutlar için DeepSeek AI ile sohbet et
            return self.api.chat_with_deepseek(command)
            
        except Exception as e:
            print(f"Komut işleme hatası: {str(e)}")
            return "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin."
    
    def search_web(self):
        query = self.show_input_dialog("Web'de Ara", "Ne aramak istiyorsunuz?")
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            self.add_message(f"Web'de '{query}' için arama yapılıyor...", False)
            
    def play_music(self):
        query = self.show_input_dialog("Müzik Aç", "Hangi müziği dinlemek istiyorsunuz?")
        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}+music")
            self.add_message(f"'{query}' müziği aranıyor...", False)
            
    def take_note(self):
        note = self.show_input_dialog("Not Al", "Notunuzu yazın:")
        if note:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            self.notes.append((timestamp, note))
            self.add_message(f"Not alındı: {note}", False)
            
    def show_notes(self):
        if not self.notes:
            self.add_message("Henüz not bulunmuyor.", False)
        else:
            notes_text = "📝 Notlarınız:\n\n"
            for timestamp, note in self.notes:
                notes_text += f"[{timestamp}]\n{note}\n\n"
            self.add_message(notes_text, False)
            
    def search_youtube(self):
        query = self.show_input_dialog("YouTube'da Ara", "Ne aramak istiyorsunuz?")
        if query:
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
            self.add_message(f"YouTube'da '{query}' için arama yapılıyor...", False)
            
    def show_input_dialog(self, title, message):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x150")
        dialog.configure(bg=self.bg_color)
        
        label = tk.Label(dialog, text=message, font=("Helvetica", 12),
                        bg=self.bg_color, fg=self.text_color)
        label.pack(pady=10)
        
        entry = tk.Entry(dialog, font=("Helvetica", 12), width=40)
        entry.pack(pady=10)
        entry.focus()
        
        result = [None]
        
        def on_ok():
            result[0] = entry.get()
            dialog.destroy()
            
        def on_enter(event):
            on_ok()
            
        ok_button = RoundedButton(dialog, "Tamam", on_ok,
                                width=100, height=35, corner_radius=15,
                                bg=self.button_color, fg="#ffffff",
                                hover_color=self.hover_color)
        ok_button.pack(pady=10)
        
        entry.bind("<Return>", on_enter)
        
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        
        return result[0]

    def clear_chat(self):
        """Sohbet geçmişini temizler"""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)
        
        # Hoş geldin mesajını tekrar ekle
        welcome_msg = (
            "👋 Merhaba! Ben Alfa, Türkçe sesli asistanınız.\n\n"
            "Size nasıl yardımcı olabilirim?\n"
            "• Hava durumu bilgisi alabilirim\n"
            "• Haberleri okuyabilirim\n"
            "• Yemek tarifi önerebilirim\n"
            "• Web'de arama yapabilirim\n"
            "• YouTube'da video arayabilirim\n"
            "• Müzik açabilirim\n"
            "• Not alabilirim\n\n"
            "Mikrofon butonuna tıklayarak veya sol menüden özellikleri kullanarak başlayabilirsiniz."
        )
        self.add_message(welcome_msg, False)
        self.add_message("Sohbet geçmişi temizlendi.", False)

def main():
    root = tk.Tk()
    app = AssistantGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()