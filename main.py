import sys
import time
import traceback

import config
from storage import load_seen, save_seen
from notifier import send_telegram_message
from scrapers import scrape_storia, scrape_publi24

# OLX e scos de-a dreptul din cod: site-ul blocheaza sistematic cererile
# venite de pe serverele GitHub Actions (eroare 403, blocare de IP,
# confirmata). Nu se poate rezolva din config.py, deci il dezactivam aici
# direct, indiferent ce scrie in config.py.
SCRAPERS = {
    "storia": scrape_storia,
    "publi24": scrape_publi24,
}

# Valori implicite in caz ca fisierul config.py de pe GitHub e o versiune
# mai veche, careia ii lipsesc unele setari noi (ca sa nu pice scriptul
# cu AttributeError daca uiti sa actualizezi config.py).
ONLY_OWNERS = getattr(config, "ONLY_OWNERS", True)
KEYWORDS_EXCLUDE = getattr(config, "KEYWORDS_EXCLUDE", [])
SOURCES = getattr(config, "SOURCES", {"storia": True, "publi24": True})


def passes_filters(ad):
    if ONLY_OWNERS and ad.get("is_agency") is True:
        return False
    title_lower = ad["title"].lower()
    for kw in KEYWORDS_EXCLUDE:
        if kw.lower() in title_lower:
            return False
    return True


def run_once(debug=False):
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("EROARE: seteaza variabilele de mediu TELEGRAM_BOT_TOKEN si "
              "TELEGRAM_CHAT_ID inainte de a rula scriptul (vezi README.md).")
        sys.exit(1)

    seen = load_seen(config.SEEN_FILE)
    first_run = len(seen) == 0
    new_ads = []

    for name, scraper_fn in SCRAPERS.items():
        if not SOURCES.get(name, True):
            continue
        try:
            ads = scraper_fn(debug=debug)
            print(f"[{name}] {len(ads)} anunturi gasite pe pagina")
        except Exception as e:
            print(f"[{name}] EROARE la scraping: {e}")
            if debug:
                traceback.print_exc()
            continue

        for ad in ads:
            if ad["id"] in seen:
                continue
            seen.add(ad["id"])
            if passes_filters(ad):
                new_ads.append(ad)

    save_seen(config.SEEN_FILE, seen)

    if first_run:
        # La prima rulare doar "inregistram" anunturile existente,
        # ca sa nu primesti notificare pentru cele ~1000+ anunturi deja postate.
        print(f"Prima rulare: am inregistrat {len(seen)} anunturi existente. "
              f"Nu trimit notificari acum — doar de la urmatoarea rulare.")
        return

    print(f"{len(new_ads)} anunturi noi de notificat.")
    for ad in new_ads:
        text = (
            f"\U0001F3E0 <b>Anunt nou - {ad['source']}</b>\n"
            f"{ad['title']}\n"
            f"Pret: {ad['price']}\n"
            f"{ad['url']}"
        )
        ok = send_telegram_message(config.TELEGRAM_BOT_TOKEN, config.TELEGRAM_CHAT_ID, text)
        print(f"  -> {ad['source']}: {'trimis' if ok else 'ESUAT'}")
        time.sleep(1)  # evitam rate-limit-ul Telegram cand sunt multe anunturi deodata


if __name__ == "__main__":
    debug_mode = "--debug" in sys.argv
    run_once(debug=debug_mode)
