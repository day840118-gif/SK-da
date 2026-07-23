# -*- coding: utf-8 -*-
"""
license.py — ប្រព័ន្ធបង្កើត និងផ្ទៀងផ្ទាត់ Activation Key (offline, no server required)

របៀបដំណើរការ:
    - Key ត្រូវបានបង្កើតដោយ 3 ក្រុមតួអក្សរចៃដន្យ + 1 ក្រុម checksum
      (HMAC-SHA256 នៃ 3 ក្រុមដំបូង ដោយប្រើ SECRET ដែលបានបង្កប់ក្នុងកម្មវិធី)
    - ការផ្ទៀងផ្ទាត់ធ្វើឡើងទាំងស្រុងនៅលើម៉ាស៊ីនអ្នកប្រើ (offline) មិនចាំបាច់មាន server ទេ។

⚠️ សំខាន់៖ នេះជាការការពារកម្រិតមូលដ្ឋាន (basic gate) សម្រាប់រៀបចំចែកចាយកម្មវិធី
ទៅកាន់អតិថិជន/អ្នកប្រើប្រាស់ដែលទុកចិត្ត។ វាមិនមែនជា DRM កម្រិតសហគ្រាសទេ ព្រោះ
Python bytecode អាច decompile បាន។ ប្រសិនបើត្រូវការសុវត្ថិភាពខ្ពស់ជាងនេះ គួរប្រើ
license server ពិតប្រាកដ (validate key + machine-id តាមអ៊ីនធឺណិត)។

សូមផ្លាស់ប្តូរ SECRET ខាងក្រោមទៅជាតម្លៃសម្ងាត់ផ្ទាល់ខ្លួនរបស់អ្នក មុននឹងចែកចាយកម្មវិធី។
"""

import hashlib
import hmac
import json
import os
import secrets
import string
import sys

# ចាំបាច់ត្រូវផ្លាស់ប្តូរតម្លៃនេះទៅជាកូដសម្ងាត់ផ្ទាល់ខ្លួនរបស់អ្នក
SECRET = b"CHANGE-ME-TO-YOUR-OWN-SECRET-2026"

ALPHABET = string.ascii_uppercase + string.digits  # គ្មាន O/0, I/1 ច្រឡំគ្នា អាចកែសម្រួលបាន
GROUP_LEN = 5
NUM_GROUPS = 3  # ក្រុមទិន្នន័យ (មិនរាប់ក្រុម checksum)


def _make_group(n=GROUP_LEN):
    return "".join(secrets.choice(ALPHABET) for _ in range(n))


def _checksum(parts, length=GROUP_LEN):
    data = "-".join(parts).encode("utf-8")
    digest = hmac.new(SECRET, data, hashlib.sha256).hexdigest().upper()
    return digest[:length]


def generate_key():
    """បង្កើត license key ថ្មីមួយ (ប្រើដោយអ្នកលក់/admin ប៉ុណ្ណោះ)."""
    parts = [_make_group() for _ in range(NUM_GROUPS)]
    chk = _checksum(parts)
    return "-".join(parts + [chk])


def validate_key(key: str) -> bool:
    """ត្រឡប់ True ប្រសិនបើ key ត្រឹមត្រូវតាមទម្រង់ និង checksum."""
    if not key:
        return False
    segments = key.strip().upper().split("-")
    if len(segments) != NUM_GROUPS + 1:
        return False
    *parts, chk = segments
    if any(len(p) != GROUP_LEN for p in parts) or len(chk) != GROUP_LEN:
        return False
    return hmac.compare_digest(_checksum(parts), chk)


# ---------------------------------------------------------------- STORAGE --
def _config_dir():
    if sys.platform.startswith("win"):
        base = os.getenv("APPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.path.expanduser("~/.config")
    path = os.path.join(base, "SK")
    os.makedirs(path, exist_ok=True)
    return path


def _license_file():
    return os.path.join(_config_dir(), "license.json")


def load_saved_key():
    """អានលេខសម្ងាត់ដែលធ្លាប់បានធ្វើ Activation ស្តេវហើយ (បើមាន)."""
    path = _license_file()
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        key = data.get("key", "")
        if validate_key(key):
            return key
    except Exception:
        pass
    return None


def save_key(key: str):
    path = _license_file()
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"key": key.strip().upper()}, f)


def is_activated():
    return load_saved_key() is not None


def activate(key: str) -> bool:
    if validate_key(key):
        save_key(key)
        return True
    return False


if __name__ == "__main__":
    # របៀបប្រើ: python license.py [ចំនួន key ដែលចង់បង្កើត]
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(f"បង្កើត {count} Activation Key(s):\n")
    for _ in range(count):
        print(generate_key())
