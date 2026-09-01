"""
Scrapere pentru OLX, Storia si Publi24.

IMPORTANT: aceste site-uri isi pot schimba structura HTML oricand, ceea ce
poate "rupe" un scraper existent. De asta fiecare functie are un fallback
si un mod --debug (vezi main.py) care iti arata cate rezultate a gasit
fiecare metoda de extractie, ca sa poti depana rapid daca ceva nu merge.

OLX si Storia au sisteme anti-bot (rate limiting / verificari de trafic).
Daca rulezi scriptul foarte des sau de pe un server cloud cu IP "suspect",
e posibil sa primesti raspunsuri goale sau erori HTTP 403. Solutii:
  - ruleaza la interval de 5-10 minute, nu mai des
  - foloseste headerele de mai jos (simuleaza un browser normal)
  - daca tot esueaza constant, ia in calcul pachetul `cloudscraper` in loc
    de `requests` pentru acele site-uri specifice
"""

import re
import json

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ro-RO,ro;q=0.9,en-US;q=0.8,en;q=0.7",
}


def _fetch(url):
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.text


# ---------------------------------------------------------------------------
# OLX
# ---------------------------------------------------------------------------

def scrape_olx(url=None, debug=False):
    from config import SEARCH_URLS
    url = url or SEARCH_URLS["olx"]

    html = _fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    results = []

    cards = soup.select('[data-cy="l-card"]')
    if debug:
        print(f"[OLX] {len(cards)} carduri gasite cu selectorul principal")

    for card in cards:
        link_tag = card.find("a", href=True)
        if not link_tag:
            continue
        href = link_tag["href"]
        if href.startswith("/"):
            href = "https://www.olx.ro" + href

        # ID-ul OLX apare de obicei in URL ca "...-IDxxxxxxx.html"
        m = re.search(r"-ID([a-zA-Z0-9]+)\.html", href)
        ad_id = m.group(1) if m else href

        title_tag = card.select_one('[data-testid="ad-title"]') or card.find(["h4", "h6"])
        title = title_tag.get_text(strip=True) if title_tag else "Anunt fara titlu"

        price_tag = card.select_one('[data-testid="ad-price"]')
        price = price_tag.get_text(strip=True) if price_tag else "N/A"

        results.append({
            "id": f"olx_{ad_id}",
            "title": title,
            "price": price,
            "url": href,
            "source": "OLX",
        })

    if not results and debug:
        print("[OLX] Niciun rezultat — structura paginii s-a putut schimba. "
              "Ruleaza cu --debug si verifica manual pagina in browser.")

    return results


# ---------------------------------------------------------------------------
# Storia (site Next.js — datele sunt de obicei intr-un JSON __NEXT_DATA__)
# ---------------------------------------------------------------------------

def scrape_storia(url=None, debug=False):
    from config import SEARCH_URLS
    url = url or SEARCH_URLS["storia"]

    html = _fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    results = []

    script = soup.find("script", id="__NEXT_DATA__")
    if script and script.string:
        try:
            data = json.loads(script.string)
            items = (
                data.get("props", {})
                    .get("pageProps", {})
                    .get("data", {})
                    .get("searchAds", {})
                    .get("items", [])
            )
            if debug:
                print(f"[Storia] {len(items)} anunturi gasite in JSON __NEXT_DATA__")
            for it in items:
                slug = it.get("slug", "")
                ad_id = it.get("id", slug)
                title = it.get("title", "Anunt fara titlu")
                price_obj = it.get("totalPrice") or {}
                price = f"{price_obj.get('value', '?')} {price_obj.get('currency', '')}".strip()
                ad_url = f"https://www.storia.ro/ro/oferta/{slug}"
                results.append({
                    "id": f"storia_{ad_id}",
                    "title": title,
                    "price": price,
                    "url": ad_url,
                    "source": "Storia",
                })
            if results:
                return results
        except Exception as e:
            if debug:
                print(f"[Storia] Parsarea JSON a esuat ({e}), trec pe fallback HTML")

    # Fallback: cauta direct linkurile catre oferte in HTML
    if debug:
        print("[Storia] Folosesc fallback bazat pe linkuri <a href='/ro/oferta/...'>")
    seen_hrefs = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/ro/oferta/" not in href or href in seen_hrefs:
            continue
        seen_hrefs.add(href)
        full_url = href if href.startswith("http") else "https://www.storia.ro" + href
        title = a.get_text(strip=True) or "Anunt fara titlu"
        results.append({
            "id": f"storia_{href}",
            "title": title,
            "price": "N/A",
            "url": full_url,
            "source": "Storia",
        })
    return results


# ---------------------------------------------------------------------------
# Publi24
# ---------------------------------------------------------------------------

def scrape_publi24(url=None, debug=False):
    from config import SEARCH_URLS
    url = url or SEARCH_URLS["publi24"]

    html = _fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    results = []
    seen_hrefs = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/anunt/" not in href or not href.endswith(".html") or href in seen_hrefs:
            continue
        seen_hrefs.add(href)

        title = a.get_text(strip=True)
        if not title:
            # unele linkuri sunt doar pe imagine, fara text -> le sarim
            continue

        full_url = href if href.startswith("http") else "https://www.publi24.ro" + href
        m = re.search(r"/([a-z0-9]{20,})\.html", href)
        ad_id = m.group(1) if m else href

        results.append({
            "id": f"publi24_{ad_id}",
            "title": title,
            "price": "N/A",
            "url": full_url,
            "source": "Publi24",
        })

    if debug:
        print(f"[Publi24] {len(results)} anunturi gasite")

    return results
