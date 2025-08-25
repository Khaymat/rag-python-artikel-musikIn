# SEO Sulap Engine 

Versi ini telah dipecah menjadi beberapa file Python untuk meningkatkan keterbacaan dan pengelolaan kode.

## Struktur File

-   `main.py`: File utama untuk menjalankan aplikasi. **Anda hanya perlu mengedit dan menjalankan file ini.**
-   `config.py`: Mengelola API Key dan koneksi ke model AI.
-   `utils.py`: Berisi fungsi-fungsi bantuan seperti pembaca file, filter teks, dan pengenal artikel.
-   `prompt_builder.py`: Khusus untuk membangun prompt kompleks yang dikirim ke AI.
-   `*.txt` & `*.html`: File data dan template yang dibutuhkan oleh skrip.

## Persiapan

1.  **Pastikan semua file** (`main.py`, `config.py`, `utils.py`, `prompt_builder.py`, dan file data Anda) berada di dalam **satu folder**.
2.  **Install Library**: Buka terminal dan jalankan:
    ```bash
    pip install beautifulsoup4 google-generativeai
    ```
3.  **Isi `gemini.txt`** dengan API Key Anda.

## Cara Menjalankan

1.  **Buka `main.py`**.
2.  **Masukkan konten HTML** artikel Anda ke dalam variabel `artikel_untuk_dioptimasi`.
3.  **Jalankan file utama** dari terminal:
    ```bash
    python main.py
    ```
4.  Hasil akhir akan dicetak di terminal.