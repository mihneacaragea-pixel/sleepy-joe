import json
import os


def load_seen(path):
    """Incarca multimea de ID-uri de anunturi deja notificate."""
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        try:
            return set(json.load(f))
        except json.JSONDecodeError:
            return set()


def save_seen(path, seen_ids):
    """Salveaza multimea de ID-uri (sortata, pentru un diff git curat)."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sorted(seen_ids), f, ensure_ascii=False, indent=2)
