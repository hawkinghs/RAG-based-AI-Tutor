import json
from datetime import datetime
from pathlib import Path


HISTORY_FILE = Path("data") / "user_history.json"


def normalize_user_id(user_name: str) -> str:
    user_name = (user_name or "default").strip()
    return user_name or "default"


def load_history(user_name: str):
    user_id = normalize_user_id(user_name)

    if not HISTORY_FILE.exists():
        return []

    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    return data.get(user_id, [])


def add_history_entry(user_name: str, entry_type: str, title: str, content: str):
    user_id = normalize_user_id(user_name)
    HISTORY_FILE.parent.mkdir(exist_ok=True)

    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, FileNotFoundError):
        data = {}

    entries = data.setdefault(user_id, [])
    entries.insert(
        0,
        {
            "type": entry_type,
            "title": title,
            "content": content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        },
    )

    data[user_id] = entries[:50]
    HISTORY_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

