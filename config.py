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
SOURCES = {
    "olx": True,
    "storia": True,
    "publi24": True,
}

# URL-urile de cautare (deja filtrate pe Craiova + apartamente de vanzare).
# Poti ajusta filtrele (pret, zona, camere) direct pe site, apoi copiezi
# URL-ul rezultat aici.
SEARCH_URLS = {
    "olx": "https://www.olx.ro/imobiliare/apartamente-garsoniere-de-vanzare/craiova/",
    "storia": "https://www.storia.ro/ro/rezultate/vanzare/apartament/dolj/craiova",
    "publi24": "https://www.publi24.ro/anunturi/imobiliare/de-vanzare/apartamente/dolj/craiova/",
}

SEEN_FILE = "seen_ids.json"
