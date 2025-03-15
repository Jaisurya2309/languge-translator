import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from deep_translator import GoogleTranslator
import speech_recognition as sr
import pyttsx3
import os
from gtts import gTTS

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("translated_audio.mp3")
        os.system("start translated_audio.mp3")
    except Exception as e:
        print(f"Speech synthesis failed: {e}")

def translate_text():
    source_text = text_input.get("1.0", tk.END).strip()
    from_lang = from_lang_var.get()
    to_lang = to_lang_var.get()
    if not source_text:
        return
    try:
        translated = GoogleTranslator(source=from_lang, target=to_lang).translate(source_text)
        output_label.config(text=translated)
        speak(translated, to_lang)
    except Exception as e:
        output_label.config(text=f"Translation failed: {e}")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            status_label.config(text="Listening...")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            text_input.delete("1.0", tk.END)
            text_input.insert(tk.END, text)
            status_label.config(text="")
        except:
            status_label.config(text="Speech not recognized.")

def swap_languages():
    from_lang_var.set(to_lang_var.get())
    to_lang_var.set(from_lang_var.get())

# GUI Setup
root = tk.Tk()
root.title("Professional Language Translator")
root.geometry("500x600")
root.configure(bg="#222")
root.resizable(False, False)

# Load Background Image
bg_image = Image.open("background.jpeg")
bg_image = bg_image.resize((500, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Style
style = ttk.Style()
style.configure("TButton", padding=10, relief="flat", background="#FF4C29", foreground="white")

# Frame to center elements
container = tk.Frame(root, bg="#333", bd=5)
container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Language selection
tk.Label(container, text="Choose Language", fg="white", bg="#333", font=("Arial", 12)).pack(pady=5)
from_lang_var = tk.StringVar(value="en")
to_lang_var = tk.StringVar(value="fr")

lang_frame = tk.Frame(container, bg="#333")
lang_frame.pack(pady=10)

from_dropdown = ttk.Combobox(lang_frame, textvariable=from_lang_var, values=list(GoogleTranslator().get_supported_languages(as_dict=True).keys()))
from_dropdown.grid(row=0, column=0)

toggle_btn = tk.Button(lang_frame, text="↔", command=swap_languages, bg="#FF4C29", fg="white")
toggle_btn.grid(row=0, column=1, padx=5)

to_dropdown = ttk.Combobox(lang_frame, textvariable=to_lang_var, values=list(GoogleTranslator().get_supported_languages(as_dict=True).keys()))
to_dropdown.grid(row=0, column=2)

# Text input
text_input = tk.Text(container, height=5, width=40, bg="#333", fg="white")
text_input.pack(pady=10)

speech_btn = tk.Button(container, text="🎤 Speak", command=recognize_speech, bg="#FF4C29", fg="white")
speech_btn.pack(pady=5)

status_label = tk.Label(container, text="", fg="white", bg="#333")
status_label.pack()

translate_btn = tk.Button(container, text="Translate", command=translate_text, bg="#FF4C29", fg="white")
translate_btn.pack(pady=10)

output_label = tk.Label(container, text="", fg="white", bg="#333", wraplength=350, font=("Arial", 12))
output_label.pack(pady=10)

root.mainloop()