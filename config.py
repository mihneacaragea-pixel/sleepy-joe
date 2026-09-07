import os

# --- Telegram ---
# Nu pune tokenul direct aici! Se citeste din variabile de mediu
# (vezi README.md pentru cum le setezi local sau in GitHub Actions).
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# --- Filtre optionale ---
# Lasa lista goala daca nu vrei sa excluzi nimic.
# Orice anunt al carui titlu contine unul din aceste cuvinte va fi ignorat.
KEYWORDS_EXCLUDE = [
    # "mansarda",
    # "schimb",
]

# --- Ce site-uri sa verifice ---
# OLX e dezactivat: blocheaza cererile venite de pe serverele GitHub
# Actions cu eroare HTTP 403 (blocare de IP, confirmata — nu se rezolva
# din headere sau cod). Daca la un moment dat rulezi scriptul de pe alt
# IP (calculator propriu, alt hosting), poti pune din nou True aici.
SOURCES = {
    "olx": False,
    "storia": True,
    "publi24": True,
    "lajumate": True,
    "homezz": True,
}

# Daca True, incearca sa pastreze DOAR anunturile postate de proprietari
# (exclude agentiile imobiliare) — pentru site-urile unde reusim sa
# distingem cat de cat sigur intre ele. Vezi README.md, sectiunea
# "Filtrul doar de la proprietari" pentru ce e fiabil si ce nu.
# NOTA: Lajumate si HomeZZ nu au niciun semnal proprietar/agentie vizibil
# pe pagina de cautare, deci pentru ele filtrul nu se aplica — vei vedea
# toate anunturile de acolo, agentii incluse.
ONLY_OWNERS = True

# URL-urile de cautare (deja filtrate pe Craiova + apartamente de vanzare).
# Poti ajusta filtrele (pret, zona, camere) direct pe site, apoi copiezi
# URL-ul rezultat aici.
#
# NOTA: am incercat initial sa adaugam parametri de genul
# "private_business=private" sau "commercial=false" ca sa cerem filtrarea
# direct de la site. Pentru Publi24 am verificat manual ca NU are niciun
# efect (lista returnata e identica, cu tot cu agentii) — filtrul lor e
# doar vizual (JavaScript), nu functioneaza la o simpla descarcare a
# paginii. L-am scos ca sa nu induca in eroare. Filtrarea proprietar/
# agentie se face acum din continutul paginii, in scrapers.py.
#
# NOTA 2: romimo.ro si imoradar24.ro NU sunt incluse — romimo.ro e
# practic aceeasi platforma/baza de date ca Publi24 (ar duplica
# notificarile), iar imoradar24.ro e un agregator care oricum scaneaza
# alte site-uri (nu aduce anunturi noi, unice).
SEARCH_URLS = {
    "olx": "https://www.olx.ro/imobiliare/apartamente-garsoniere-de-vanzare/craiova/",
    "storia": "https://www.storia.ro/ro/rezultate/vanzare/apartament/dolj/craiova",
    "publi24": "https://www.publi24.ro/anunturi/imobiliare/de-vanzare/apartamente/dolj/craiova/",
    "lajumate": "https://lajumate.ro/anunturi/imobiliare/apartamente-de-vanzare/in/dolj/craiova",
    "homezz": "https://homezz.ro/vanzare-apartamente/craiova-dj",
}

SEEN_FILE = "seen_ids.json"
