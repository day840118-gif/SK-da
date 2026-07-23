; ============================================================
;  SKSetup.iss
;  Inno Setup script — បង្កើត Installer (.exe) សម្រាប់ Windows
;
;  ត្រូវការ: ដំឡើង Inno Setup Compiler (ឥតគិតថ្លៃ) ពី
;            https://jrsoftware.org/isdl.php
;
;  របៀបប្រើ:
;    1. រត់ build_exe.bat ជាមុនសិន ដើម្បីបង្កើត app\dist\SK.exe
;    2. បើកឯកសារនេះជាមួយ Inno Setup Compiler (ISCC.exe ឬ GUI)
;    3. ចុច Compile → នឹងបានឯកសារ Setup នៅក្នុងថត installer\Output\
; ============================================================

#define MyAppName "SK"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "YourCompanyName"
#define MyAppExeName "SK.exe"

[Setup]
AppId={{B6C9F5E2-7A31-4F8E-9C3D-YTDLPRO0001}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=Output
OutputBaseFilename=SKSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
SetupIconFile=..\chrome_extension\icons\app_icon.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "បង្កើត Shortcut លើ Desktop"; GroupDescription: "Shortcuts:"

[Files]
Source: "..\app\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; ចម្លងគម្រូ Chrome Extension ជាមួយកម្មវិធីផងដែរ ដើម្បីឲ្យអតិថិជនងាយស្រួល Load Unpacked
Source: "..\chrome_extension\*"; DestDir: "{app}\chrome_extension"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "បើក {#MyAppName} ឥឡូវនេះ"; Flags: nowait postinstall skipifsilent
