import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def atur_model_ai():
    """Mencari API Key dari gemini.txt dan mengonfigurasi model AI."""
    try:
        with open('gemini.txt', 'r') as f:
            api_key = f.read().strip()
        if not api_key or api_key == "Taruh Api Disini":
            raise ValueError("API Key tidak valid atau masih default.")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-pro')
        print("Berhasil no kendala.")
        return model
        
    except FileNotFoundError:
        print("GAGAL: File 'gemini.txt' tidak ditemukan. Buat dulu.")
        return None
    except ValueError as e:
        print(f"GAGAL: {e}. Periksa isi file 'gemini.txt'.")
        return None
    except Exception as e:
        print(f"GAGAL mengonfigurasi model AI. Detail: {e}")
        return None

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}