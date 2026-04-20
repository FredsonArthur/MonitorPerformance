; Script do Inno Setup para o Monitor de Performance v1.1.4
[Setup]
AppId={{C789B123-A123-4ABC-A123-456789ABCDEF}
AppName=Monitor de Performance
AppVersion=1.1.5
AppPublisher=Fredson Arthur
DefaultDirName={autopf}\MonitorPerformance
DefaultGroupName=Monitor de Performance
AllowNoIcons=yes
PrivilegesRequired=admin
; Caminho do ícone para o instalador e atalhos
SetupIconFile=src\assets\monitor.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Nome do arquivo final que você vai baixar
OutputBaseFilename=Setup_MonitorPerformance_v1.1.4

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Pega todos os arquivos gerados pelo PyInstaller (modo --onedir)
Source: "dist\MonitorPerformance_v1.1.5\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Monitor de Performance"; Filename: "{app}\MonitorPerformance_v1.1.4.exe"
Name: "{commondesktop}\Monitor de Performance"; Filename: "{app}\MonitorPerformance_v1.1.4.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MonitorPerformance_v1.1.5.exe"; Description: "{cm:LaunchProgram,Monitor de Performance}"; Flags: nowait postinstall skipifsilent