import re
from bs4 import BeautifulSoup

def muat_template(tipe_artikel):
    """Memuat konten dari file HTML template (fundamental) yang sesuai."""
    nama_file = f"{tipe_artikel.lower()}_fundamental.html"
    try:
        with open(nama_file, 'r', encoding='utf-8') as f:
            return f.read(), None
    except FileNotFoundError:
        return None, f"ERROR: File template '{nama_file}' tidak ditemukan."

def kenali_tipe_artikel(artikel_mentah):
    """Mengidentifikasi tipe artikel (makna, lirik, chord) dari kontennya."""
    soup = BeautifulSoup(artikel_mentah, 'html.parser')
    teks_untuk_dicek = ""
    if p_tag := soup.find('p'): teks_untuk_dicek += p_tag.get_text().lower()
    if h2_tag := soup.find('h2'): teks_untuk_dicek += " " + h2_tag.get_text().lower()
    
    if "chord" in teks_untuk_dicek or "kunci gitar" in teks_untuk_dicek: return "chord"
    if "lirik" in teks_untuk_dicek: return "lirik"
    if "makna lagu" in teks_untuk_dicek: return "makna"
    return None

def muat_data_afiliasi():
    """Membaca semua produk dari affiliate.txt."""
    try:
        with open('affiliate.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        daftar_produk_str = ""
        for i in range(0, len(lines), 3):
            if i + 2 < len(lines):
                daftar_produk_str += f"- Nama: {lines[i]}, URL: {lines[i+1]}, Terjual: {lines[i+2]}\n"
        
        return (daftar_produk_str, None) if daftar_produk_str else (None, "Isi file afiliasi kosong.")
    except FileNotFoundError:
        return None, "File 'affiliate.txt' tidak ditemukan."
    except Exception as e:
        return None, f"Gagal memproses file afiliasi: {e}"

def filter_konten(teks: str) -> str:
    """Membersihkan artikel dari kata-kata yang berpotensi memicu filter keamanan. Silahkan tambahkan atau modifikasi"""
    kata_kotor = {
        "fuck": "messed up", "fucks": "messed up", "fucked": "messed up", "fucker": "rude person", "fuckers": "rude people",
        "fucking": "messed up", "motherfucker": "really awful person", "motherfucking": "really awful person",
        "fuck off": "go away rudely", "fuck you": "go away rudely", "fuckin": "messed up", "frick": "mild expletive",
        "fricking": "mild expletive", "frickin": "mild expletive", "shit": "stuff", "shits": "stuff", "shitted": "stuff",
        "shitting": "stuff", "shithead": "nasty person", "shitface": "nasty person", "shitshow": "chaotic mess",
        "shitstorm": "big chaos", "crap": "nonsense", "crappy": "poor quality", "bullshit": "nonsense",
        "bollocks": "nonsense", "ass": "rear", "asses": "rears", "asshole": "jerk", "assholes": "jerks",
        "asshat": "jerk", "asswipe": "jerk", "dick": "jerk", "dicks": "jerks", "dickhead": "jerk",
        "dickheads": "jerks", "cock": "offensive word", "cockhead": "offensive person", "cunt": "offensive word",
        "prick": "jerk", "pricks": "jerks", "bitch": "heck", "bitches": "people being rude",
        "son of a bitch": "very rude person", "bastard": "unpleasant person", "bastards": "unpleasant people",
        "slut": "promiscuous person", "whore": "sex worker (neutral)", "whores": "sex workers (neutral)",
        "twat": "jerk", "wanker": "jerk", "wankers": "jerks", "tosser": "jerk", "jackass": "fool",
        "butthead": "fool", "buttface": "fool", "butt": "rear", "douche": "jerk", "douchebag": "jerk",
        "douchecanoe": "jerk", "scumbag": "scummy person", "scumbags": "scummy people", "turd": "nasty person",
        "turdface": "nasty person", "dipshit": "fool", "stfu": "be quiet", "gtfo": "get out",
        "piss off": "go away rudely", "pissed off": "angry", "piss": "urine/anger", "pissed": "angry",
        "screw you": "go away rudely", "screw off": "go away rudely", "eat shit": "go away rudely",
        "eat a dick": "go away rudely", "idiot": "unwise person", "idiots": "unwise people", "moron": "unwise person",
        "morons": "unwise people", "imbecile": "unwise person", "dumbass": "fool", "dumbasses": "fools",
        "loser": "unsuccessful person", "losers": "unsuccessful people", "trash": "rubbish", "garbage": "rubbish",
        "trashbag": "rubbish person", "garbagehead": "rubbish person", "shitfaced": "very drunk",
        "clusterfuck": "complete mess", "cluster fuck": "complete mess", "fuckery": "nonsense", "fubar": "complete mess",
        "goddamn": "darn", "goddamnit": "darn it", "damn": "darn", "dammit": "darn it", "damned": "darned",
        "holy shit": "oh no (mild)", "bull shit": "nonsense", "bull-shit": "nonsense", "shit bag": "nasty person",
        "shit face": "nasty person", "screw": "dismiss", "screwup": "mess", "screw-up": "mess",
        "crappy ass": "poor quality", "ass clown": "fool", "butt head": "fool", "dumb": "bumd",
        "kontol": "kata yang tidak pantas", "kontols": "kata yang tidak pantas", "kontolmu": "kata yang tidak pantas",
        "kontol lo": "kata yang tidak pantas", "kontol banget": "kata yang tidak pantas", "kontol lah": "kata yang tidak pantas",
        "kontolku": "kata yang tidak pantas", "memek": "kata yang tidak pantas", "memekmu": "kata yang tidak pantas",
        "memek lo": "kata yang tidak pantas", "memek banget": "kata yang tidak pantas", "memek lah": "kata yang tidak pantas",
        "anjing": "ekspresi kasar", "anjingnya": "ekspresi kasar", "anjing banget": "ekspresi kasar",
        "anjing lo": "ekspresi kasar", "anjinglah": "ekspresi kasar", "anjingmu": "ekspresi kasar",
        "bangsat": "kata kasar", "bangsat banget": "kata kasar", "bangsat lo": "kata kasar",
        "bajingan": "orang yang sangat tidak sopan", "bajingan lo": "orang yang sangat tidak sopan",
        "bajinganmu": "orang yang sangat tidak sopan", "brengsek": "orang yang sangat tidak sopan",
        "brengsek lo": "orang yang sangat tidak sopan", "brengsek banget": "orang yang sangat tidak sopan",
        "brengsekmu": "orang yang sangat tidak sopan", "kampret": "kata makian", "kampret lo": "kata makian",
        "kampret banget": "kata makian", "bacot": "mulut yang banyak bicara", "bacot lo": "mulut yang banyak bicara",
        "bacot banget": "mulut yang banyak bicara", "tolol": "kurang bijak", "tolol banget": "kurang bijak",
        "tololmu": "kurang bijak", "tolol lah": "kurang bijak", "goblok": "kurang bijak",
        "goblok banget": "kurang bijak", "goblok lo": "kurang bijak", "bego": "kurang bijak", "bego lo": "kurang bijak",
        "bego banget": "kurang bijak", "bodoh": "kurang bijak", "bodohnya": "kebodohan", "bodoh banget": "kebodohan",
        "sialan": "sial/menyedihkan", "sialan lo": "sial/menyedihkan", "sial": "sial/menyedihkan",
        "sial banget": "sangat sial", "tai": "kata kotor", "taik": "kata kotor", "tai lo": "kata kotor",
        "tai banget": "kata kotor", "asu": "kata kasar (Jawa)", "asu lo": "kata kasar (Jawa)",
        "asu banget": "kata kasar (Jawa)", "jancuk": "kata kasar (Jawa)", "jancuk lo": "kata kasar (Jawa)",
        "jancuk banget": "kata kasar (Jawa)", "setan": "kata seru kasar", "anjrit": "kata seru kasar",
        "edan": "gila (kasar)", "edan lo": "gila (kasar)", "cupu": "kurang keren", "cupu banget": "kurang keren",
        "kampungan": "tidak modern", "kampungan lo": "tidak modern", "kampungan banget": "tidak modern",
        "munafik": "hipokrit", "kolot": "kuno", "sinting": "kurang waras (kasar)", "gila": "tidak waras",
        "gila banget": "sangat", "ndasmu": "kata makian (kepala)", "ndasmu lo": "kata makian (kepala)",
        "bejad": "amat buruk", "bangke": "kata kasar (bangkai)", "bangke banget": "kata kasar",
        "keparat": "kata kasar", "anjim": "slang kasar", "pengecut": "tak berani", "pengecut lo": "tak berani",
        "sundal": "kata kotor untuk pekerja seks", "sundal lo": "kata kotor untuk pekerja seks",
        "pelacur": "pekerja seks (netral)", "pelacur lo": "pekerja seks (netral)", "curang": "tidak jujur",
        "idiot": "kurang bijak", "idiot lo": "kurang bijak", "gobloklah": "kasar", "jelek banget": "sangat buruk",
        "banci": "kata yang menyinggung (hindari penggunaan)", "bajingan banget": "sangat kasar",
        "kontol lah": "kata yang tidak pantas", "memek lah": "kata yang tidak pantas", "bodoh lah": "kasar",
        "brengsek lah": "kasar", "anjinglah": "kasar", "jancuklah": "kasar", "sampah": "rubbish person",
        "payah": "buruk", "goblokmu": "kasar", "bajinganmu": "kasar", "asu mu": "kata kasar",
        "tolol anjrit": "kombinasi kasar", "bego loh": "kasar", "goblok loh": "kasar",
        "sundal loh": "kasar", "kontolku lo": "kata yang tidak pantas"
    }
    for kata, pengganti in kata_kotor.items():
        teks = re.sub(r'\b' + re.escape(kata) + r'\b', pengganti, teks, flags=re.IGNORECASE)
    return teks