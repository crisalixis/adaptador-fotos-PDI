[Setup]
AppName=AdaptadorDeFotos
AppVersion=1.0
DefaultDirName={pf}\AdaptadorDeFotos
DefaultGroupName=AdaptadorDeFotos
OutputBaseFilename=AdaptadorDeFotosInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\Tania\Desktop\workspace\Adaptador\dist\adaptador.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AdaptadorDeFotos"; Filename: "{app}\adaptador.exe"
Name: "{group}\Desinstalar Adaptador"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\adaptador.exe"; Description: "Ejecutar AdaptadorDeFotos"; Flags: nowait postinstall
