#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_keys.py — ឧបករណ៍សម្រាប់ម្ចាស់កម្មវិធី (Admin) បង្កើត Activation Key
ដើម្បីលក់ ឬចែកចាយទៅកាន់អតិថិជន។

⚠️ កុំចែកចាយឯកសារនេះ ឬ app/license.py ជាមួយកម្មវិធីដែលបញ្ជូនទៅអតិថិជន —
រក្សាទុកវានៅឯកជនសម្រាប់អ្នកគ្រប់គ្រងតែប៉ុណ្ណោះ។

របៀបប្រើ:
    python generate_keys.py            # បង្កើត 5 key
    python generate_keys.py 20         # បង្កើត 20 key
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "app"))

import license as lic  # noqa: E402

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(f"===== បង្កើត {count} Activation Key(s) សម្រាប់ SK =====\n")
    keys = [lic.generate_key() for _ in range(count)]
    for k in keys:
        print(k)

    out_path = os.path.join(os.path.dirname(__file__), "generated_keys.txt")
    with open(out_path, "a", encoding="utf-8") as f:
        f.write("\n".join(keys) + "\n")
    print(f"\n✅ បានរក្សាទុកបញ្ជី key ទាំងអស់នៅ: {out_path}")
