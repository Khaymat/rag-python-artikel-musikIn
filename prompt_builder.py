def buat_master_prompt(tipe, konten_fundamental, artikel_untuk_optimasi, tanggal_sekarang, daftar_afiliasi_str):
    """Membangun prompt lengkap dengan semua aturan presisi dari notebook asli."""

    instruksi_afiliasi = ""
    if daftar_afiliasi_str:
        instruksi_afiliasi = f"""
    7.  **SISIPKAN IKLAN (AFILIASI):** Di bawah ini adalah daftar produk.
        --- DAFTAR PRODUK ---
        {daftar_afiliasi_str}
        --- AKHIR DAFTAR ---
        Tugasmu: Pilih **SATU** produk yang paling relevan dengan lagu, lalu di bagian **MeLirik Lagu**, sisipkan **SATU kalimat natural** untuk mempromosikan produk itu. Pastikan link dalam format HTML: `<a href="URL_PRODUK">NAMA_PRODUK</a>`.
    """

    instruksi_faq_fix = """
    **INSTRUKSI PENTING UNTUK BAGIAN FAQ:**
    -   Saat membuat daftar FAQ, Anda **WAJIB** mengikuti format HTML di bawah ini.
    -   Pastikan semua pertanyaan berada di dalam **SATU** blok `<ol>` dan masing-masing pertanyaan dibungkus dengan `<li>`. JANGAN membuat `<ol>` baru untuk setiap `<li>`.

        **CONTOH FORMAT HTML FAQ (GUNAKAN INI):**
        ```html
        <ol>
        <li><a href="URL_SUMBER_1">Pertanyaan FAQ 1?</a></li>
        <li><a href="URL_SUMBER_2">Pertanyaan FAQ 2?</a></li>
        <li><a href="URL_SUMBER_3">Pertanyaan FAQ 3?</a></li>
        </ol>
        ```
    """

    instruksi_youtube_fix = """
    8.  **REPLIKASI YOUTUBE EMBED:** Temukan URL video YouTube dari "ARTIKEL UNTUK DIOPTIMASI". Kemudian, salin blok `<figure>` atau `<iframe>` yang berisi video YouTube dari "CONTOH EMAS", dan **ganti URL di dalamnya** dengan URL yang kamu temukan dari artikel sumber.
    """

    template_tabel_interaksi = """
<figure class="wp-block-table"><table><thead><tr><th>No.</th><th>👀</th><th>👍</th><th>💬</th><th>Tanggal</th></tr></thead><tbody><tr><td>1</td><td>{VIEWS_LAMA}</td><td>{LIKES_LAMA}</td><td>{COMMENTS_LAMA}</td><td>{TANGGAL_LAMA}</td></tr><tr><td>2</td><td>{VIEWS_BARU}</td><td>{LIKES_BARU}</td><td>{COMMENTS_BARU}</td><td>{TANGGAL_BARU}</td></tr><tr><td>...</td><td></td><td></td><td></td><td></td></tr><tr><td>27</td><td></td><td></td><td></td><td></td></tr></tbody></table></figure>
"""

    instruksi_cta_fix = """
    6.  **GUNAKAN CTA (Call to Action) YANG TEPAT:** Di akhir bagian lirik/makna/chord, sisipkan CTA yang sesuai. **ATURAN PENTING:**
        -   URL untuk CTA ini harus kamu buat secara dinamis dengan format `https://musikin.kekitaan.com/{slug-target}/?click=phpapl`.
        -   Jika tipe artikel **Lirik**, CTA-nya adalah "Cari chord gampangnya? Genjreng di sini [link]". Buat `{slug-target}` merujuk ke halaman **chord** lagu tersebut.
        -   Jika tipe artikel **Chord**, CTA-nya adalah "Apa sih makna dari lagu ini? [link]". Buat `{slug-target}` merujuk ke halaman **makna lagu** tersebut.
        -   Jika tipe artikel **Makna**, CTA-nya adalah "Udah tau maknanya? Nih chord gampangnya [link]". Buat `{slug-target}` merujuk ke halaman **chord** lagu tersebut.
        -   Parameter `?click=phpapl` **WAJIB** ada di akhir URL CTA ini. Parameter ini **TIDAK BOLEH** ditambahkan ke link sumber di bagian FAQ.
    """

    return f"""
    **PERAN DAN TUJUAN:**
    Anda adalah **Mesin Replikasi Template Gutenberg**. Tugas Anda adalah MEREPLIKASI STRUKTUR dari "CONTOH EMAS" secara teknis dan absolut.

    **INFORMASI PENTING HARI INI:**
    - **TANGGAL HARI INI:** {tanggal_sekarang}.

    **TEMPLATE WAJIB (STANDAR EMAS):**
    --- CONTOH EMAS ({tipe.upper()}) ---
    {konten_fundamental}
    --- AKHIR CONTOH EMAS ---

    **BAHAN MENTAH (SUMBER DATA):**
    --- ARTIKEL UNTUK DIOPTIMASI ---
    {artikel_untuk_optimasi}
    --- AKHIR ARTIKEL UNTUK DIOPTIMASI ---

    **INSTRUKSI TEKNIS LANGKAH-DEMI-LANGKAH:**
    1.  Validasi semua data inti.
    2.  Ekstrak data interaksi video LAMA.
    3.  Cari data interaksi YouTube TERBARU. 
        -   **PERINTAH ABSOLUT UNTUK BLOK INTERAKSI VIDEO:**
        -   Anda **WAJIB** menggunakan template HTML mentah di bawah ini. JANGAN membuat tabel sendiri.
        -   Ganti placeholder `{{...}}` dengan data yang sesuai.
        -   `{{VIEWS_LAMA}}`, `{{LIKES_LAMA}}`, `{{COMMENTS_LAMA}}`, `{{TANGGAL_LAMA}}` diisi dengan data yang Anda ekstrak dari artikel asli.
        -   `{{VIEWS_BARU}}`, `{{LIKES_BARU}}`, `{{COMMENTS_BARU}}` diisi dengan data riset terbaru Anda.
        -   `{{TANGGAL_BARU}}` diisi dengan tanggal hari ini: **{tanggal_sekarang}**.

        **TEMPLATE TABEL MENTAH (GUNAKAN INI):**
        ```html
        {template_tabel_interaksi}
        ```
    4.  Riset SATU SUMBER UTAMA untuk makna lagu.
    5.  Buat 5 Pertanyaan FAQ dari 5 SUMBER BERBEDA.
    {instruksi_cta_fix}
    {instruksi_afiliasi}
    {instruksi_youtube_fix}

    {instruksi_faq_fix}

    **LANGKAH FINAL: FORMAT OUTPUT**
    - Output HANYA kode Gutenberg final dalam format JSON dengan key tunggal: `"kode_gutenberg_final"`.
    -  **PENTING**: Pastikan nilai untuk `"kode_gutenberg_final"` adalah string JSON yang valid, artinya semua tanda kutip ganda ("") dan karakter khusus lainnya di dalam konten HTML harus di-escape dengan benar.
    """