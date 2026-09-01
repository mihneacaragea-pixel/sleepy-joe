import requests


def send_telegram_message(token, chat_id, text):
    """Trimite un mesaj text (HTML) catre un chat Telegram. Returneaza True/False."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        resp = requests.post(url, data=payload, timeout=15)
    except requests.RequestException as e:
        print(f"[EROARE Telegram] Nu am putut trimite mesajul: {e}")
        return False

    if resp.status_code != 200:
        print(f"[EROARE Telegram] {resp.status_code}: {resp.text}")
        return False
    return True
