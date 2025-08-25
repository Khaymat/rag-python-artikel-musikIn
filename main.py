import json
import re
import locale
from datetime import datetime

from config import atur_model_ai, SAFETY_SETTINGS
from utils import muat_template, kenali_tipe_artikel, muat_data_afiliasi, filter_konten
from prompt_builder import buat_master_prompt

def jalankan_optimasi_seo(artikel_mentah):
    """Fungsi utama yang menjalankan seluruh proses optimasi artikel."""
    try:
        locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
    except locale.Error:
        print("Peringatan: Locale 'id_ID.UTF-8' tidak ditemukan. Format tanggal mungkin Inggris.")
        
    model = atur_model_ai()
    if not model: return

    if not artikel_mentah or not artikel_mentah.strip():
        print("Artikel untuk dioptimasi masih kosong. Harap isi dengan konten HTML.")
        return
        
    print("[1] Memfilter konten dan mengenali tipe artikel...")
    artikel_aman = filter_konten(artikel_mentah)
    tipe_artikel = kenali_tipe_artikel(artikel_aman)
    if not tipe_artikel:
        print("GAGAL: Tidak dapat mengidentifikasi tipe artikel (lirik/chord/makna).")
        return
    print(f"    -> Tipe: {tipe_artikel.capitalize()}")

    template_konten, error = muat_template(tipe_artikel)
    if error: print(f"❌ {error}"); return
    print("    -> Template dimuat.")
    
    data_afiliasi, error_afiliasi = muat_data_afiliasi()
    if error_afiliasi: print(f"    -> ⚠️ {error_afiliasi}")
    else: print("    -> Afiliasi dimuat.")

    tanggal_hari_ini = datetime.now().strftime("%A, %d %B %Y")
    print(f"[2] Membangun Master Prompt (Tanggal: {tanggal_hari_ini})...")
    master_prompt = buat_master_prompt(tipe_artikel, template_konten, artikel_aman, tanggal_hari_ini, data_afiliasi)

    print("\n[3] Optimasi...")
    try:
        response = model.generate_content(master_prompt, safety_settings=SAFETY_SETTINGS)
        cleaned_response = re.sub(r'^```json\s*|\s*```$', '', response.text.strip(), flags=re.MULTILINE)
        hasil_json = json.loads(cleaned_response)

        print("\n" + "="*60 + "\n🎉 PROSES SULAP SEO SELESAI 🎉\n" + "="*60)
        print("\n## 💻 KODE GUTENBERG FINAL (SIAP PAKAI) ##\n" + "-" * 60 + "\n")
        print(hasil_json.get("kode_gutenberg_final", "Tidak ada kode yang dihasilkan."))
        
    except json.JSONDecodeError:
        print(f"\nGAGAL: AI tidak memberikan output JSON yang valid. Coba lagi.")
        print("--- RAW RESPONSE DARI AI ---\n", response.text)
    except Exception as e:
        print(f"\nGAGAL: Detail: {e}")
        if 'response' in locals() and hasattr(response, 'prompt_feedback'):
            print(f"    Feedback AI: {response.prompt_feedback}")


if __name__ == "__main__":
    # Ganti isi variabel ini dengan konten HTML lengkap dari artikel yang ingin dioptimasi.
    artikel_untuk_dioptimasi = """
    """
    
    jalankan_optimasi_seo(artikel_untuk_dioptimasi)