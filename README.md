# SK

កម្មវិធីទាញយកវីដេអូ YouTube ស្រដៀង IDM មាន៖
- ✅ ប្រព័ន្ធ **Activation Key** (offline, គ្មានតម្រូវការ server)
- ✅ **Chrome Extension** ដែលបន្ថែមប៊ូតុងទាញយកផ្ទាល់លើទំព័រ YouTube
- ✅ អាចបង្កើតជា **Installer (.exe)** សម្រាប់ Windows

```
ytpro/
├── app/                     ← កម្មវិធី Desktop (Python)
│   ├── sk.py
│   ├── license.py           ← ប្រព័ន្ធ Activation Key
│   ├── server.py            ← Local server ភ្ជាប់ជាមួយ Chrome Extension
│   └── requirements.txt
├── chrome_extension/        ← Chrome Extension
│   ├── manifest.json
│   ├── background.js / popup.js / content.js
│   └── icons/
├── installer/                ← ឯកសារសម្រាប់ build Windows installer
│   ├── build_exe.bat
│   └── SKSetup.iss
└── generate_keys.py          ← ឧបករណ៍ Admin បង្កើត Activation Key
```

---

## ១. របៀបប្រើប្រាស់ភ្លាមៗ (Run from source)

```bash
cd app
pip install -r requirements.txt
python sk.py
```

ដំឡើង **FFmpeg** ជាមុន (ត្រូវការសម្រាប់គុណភាពខ្ពស់ + MP3)៖
- Windows: `choco install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`

លើកដំបូងបើក កម្មវិធីនឹងសុំ **Activation Key** ។ សូមបង្កើត key សាកល្បងដោយ៖

```bash
python generate_keys.py 1
```

រួចចម្លង key ដែលបានបង្កើត បញ្ចូលទៅក្នុងប្រអប់ Activation។

---

## ២. ការគ្រប់គ្រង Activation Key (សម្រាប់ម្ចាស់កម្មវិធី)

- ឯកសារ `generate_keys.py` (root) និង `app/license.py` គឺសម្រាប់ **អ្នកគ្រប់គ្រង/លក់** ប៉ុណ្ណោះ។
  កុំចែកចាយ `generate_keys.py` ជាមួយកម្មវិធីទៅកាន់អតិថិជន។
- បើកឯកសារ `app/license.py` រកបន្ទាត់៖
  ```python
  SECRET = b"CHANGE-ME-TO-YOUR-OWN-SECRET-2026"
  ```
  **ត្រូវផ្លាស់ប្តូរតម្លៃនេះ** ទៅជាកូដសម្ងាត់ផ្ទាល់ខ្លួនរបស់អ្នក មុននឹង build/ចែកចាយកម្មវិធី
  (បើមិនប្តូរ អ្នកដទៃដែលដឹង secret លំនាំដើមអាចបង្កើត key ក្លែងក្លាយបាន)។
- បង្កើត key ថ្មីៗសម្រាប់អតិថិជនម្នាក់ៗ៖ `python generate_keys.py 10`
- ⚠️ ចំណាំ៖ នេះជាការការពារកម្រិតមូលដ្ឋាន (basic license gate) សមរម្យសម្រាប់ចែកចាយក្នុងវិសាលភាពតូច។
  វាមិនមែនជា DRM កម្រិតសហគ្រាសទេ ព្រោះ Python អាច decompile បាន។ បើត្រូវការសុវត្ថិភាពខ្ពស់ជាង
  គួរប្រើ license server ពិតប្រាកដ ដែលផ្ទៀងផ្ទាត់តាមអ៊ីនធឺណិត។

---

## ៣. បង្កើត Installer (.exe) សម្រាប់ Windows

មាន ២ វិធីៈ

### វិធីទី ១ (ស្រួលបំផុត — មិនចាំបាច់មាន Windows PC ផ្ទាល់ខ្លួន) — GitHub Actions

ខ្ញុំបានរៀបចំ workflow ស្វ័យប្រវត្តិឲ្យរួចហើយ (`.github/workflows/build-windows-exe.yml`)
ដែលនឹង build ឯកសារ `SK.exe` ជូនអ្នកនៅលើ server របស់ GitHub ដោយឥតគិតថ្លៃ។

1. បង្កើត account GitHub (បើមិនទាន់មាន) — https://github.com/signup
2. បង្កើត repository ថ្មី (ចុច **New repository**, ដាក់ឈ្មោះអ្វីក៏បាន, ជ្រើស **Private** បើចង់)
3. ក្នុងទំព័រ repository ថ្មី ចុច **"uploading an existing file"** រួច **អូស (drag & drop)**
   ថតទាំងមូល `ytpro/` (ឬឯកសារទាំងអស់ក្នុងវា) ចូល រួចចុច **Commit changes**
4. ចូលទៅ tab **Actions** នៅផ្នែកខាងលើ repository → នឹងឃើញ workflow "Build SK Windows EXE"
   កំពុងរត់ស្វ័យប្រវត្តិ (ចាំប្រហែល ២-៣ នាទី)
5. ពេលរួច ចុចចូល workflow run នោះ → រំកិលចុះក្រោម → ចុច **"SK-windows-exe"**
   ក្នុងផ្នែក **Artifacts** → នឹងទាញយកជា zip ដែលមាន `SK.exe` ពិតប្រាកដសម្រាប់ Windows ក្នុងនោះ

✅ វិធីនេះមិនចាំបាច់មាន Windows PC ទាល់តែសោះ — GitHub ជាអ្នក build ជំនួសអ្នក។

### វិធីទី ២ — Build ដោយផ្ទាល់លើ Windows PC

### ជំហានទី ១ — Build ជា .exe មួយឯកតែម្នាក់ (portable)
1. ចម្លងទាំងថត `ytpro/` ទៅកុំព្យូទ័រ Windows
2. ដំឡើង [Python 3.9+](https://www.python.org/downloads/) (ជ្រើស "Add to PATH")
3. ដាប់ Double-click លើ `installer\build_exe.bat`
   → នឹងបាន `app\dist\SK.exe` ដែលអាចចែកចាយផ្ទាល់បាន (portable, គ្មានចាំបាច់ដំឡើង Python)

### ជំហានទី ២ — Build ជា Setup Installer ពិតប្រាកដ (ស្រេចចិត្ត)
1. ដំឡើង [Inno Setup Compiler](https://jrsoftware.org/isdl.php) (ឥតគិតថ្លៃ)
2. បើកឯកសារ `installer\SKSetup.iss`
3. កែ `MyAppPublisher` ជាឈ្មោះក្រុមហ៊ុន/ម្ចាស់កម្មវិធីរបស់អ្នក
4. ចុច **Build → Compile**
   → នឹងបាន `installer\Output\SKSetup.exe` ជា Installer ពេញលេញ
   (មាន Wizard, Desktop Shortcut, Uninstaller, ហើយចម្លង Chrome Extension ភ្ជាប់ជាមួយស្រាប់)

---

## ៤. ដំឡើង Chrome Extension

Google Chrome មិនអនុញ្ញាតបោះពុម្ភ Extension ប្រភេទទាញយកវីដេអូ YouTube នៅលើ Chrome
Web Store ដោយផ្ទាល់ទេ (ផ្ទុយនឹងគោលការណ៍របស់ YouTube) ដូច្នេះត្រូវដំឡើងតាមរបៀប
**"Load unpacked"** (Developer Mode) ដូចខាងក្រោម៖

1. បើក Chrome ចូល `chrome://extensions`
2. បើក **Developer mode** (ជ្រុងខាងស្តាំខាងលើ)
3. ចុច **Load unpacked**
4. ជ្រើសរើសថត `chrome_extension/` (ឬ `{ទីតាំងដំឡើង}\chrome_extension` បើប្រើ Installer)
5. Icon កម្មវិធីនឹងបង្ហាញនៅលើ toolbar របស់ Chrome

**របៀបប្រើ:**
- បើកកម្មវិធី **SK** លើ Desktop ជាមុន (ត្រូវឲ្យវារត់ក្នុងផ្ទៃខាងក្រោយ)
- ចូលទំព័រវីដេអូ YouTube ណាមួយ → នឹងឃើញប៊ូតុងអណ្តែត **"⬇ ទាញយក"** ជ្រុងខាងស្តាំក្រោម
- ឬចុច Icon extension លើ toolbar → ចុច **"ទាញយកវីដេអូនេះ"**
- Extension នឹងផ្ញើតំណវីដេអូទៅកម្មវិធី Desktop (តាមរយៈ `http://127.0.0.1:8765`)
  ហើយកម្មវិធី Desktop ជាអ្នកទាញយកជាក់ស្តែងតាមរយៈ yt-dlp

**ហេតុអ្វី Extension មិនទាញយកផ្ទាល់ដោយខ្លួនឯង?**
YouTube អ៊ិនគ្រីប streaming URLs ហើយផ្លាស់ប្តូររាល់ថ្ងៃ — ត្រូវការ engine ដូច yt-dlp
ដែលដំណើរការនៅលើ Desktop ដើម្បីទាញយកបានត្រឹមត្រូវ។ Extension ដើរតួជា "remote control"
ភ្ជាប់ទៅកម្មវិធី Desktop ប៉ុណ្ណោះ។

---

## ៥. ចំណាំផ្នែកច្បាប់ (Legal Note)

សូមប្រើកម្មវិធីនេះដើម្បីទាញយកតែមាតិកាដែលអ្នកមានសិទ្ធិស្របច្បាប់ (វីដេអូផ្ទាល់ខ្លួន,
Creative Commons, ឬបានទទួលការអនុញ្ញាតច្បាស់លាស់ពីម្ចាស់)។ ការទាញយកមាតិកាដែលមាន
កម្មសិទ្ធិបញ្ញាដោយគ្មានការអនុញ្ញាតអាចផ្ទុយនឹងលក្ខខណ្ឌប្រើប្រាស់របស់ YouTube និងច្បាប់
រក្សាសិទ្ធិនៅតំបន់របស់អ្នក។ អ្នកអភិវឌ្ឍន៍/អ្នកចែកចាយកម្មវិធីនេះទទួលខុសត្រូវលើការប្រើប្រាស់
ស្របតាមច្បាប់ដែលពាក់ព័ន្ធ។
