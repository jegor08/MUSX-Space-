[Setup]
AppName=MusX Space
AppVersion=0.1
DefaultDirName={localappdata}\MusX Space
PrivilegesRequired=lowest
OutputDir=output
OutputBaseFilename=MusX_Space_Setup
SetupIconFile=musx.ico
[Files]
Source: "dist\MusX Space.exe"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{autodesktop}\MusX Space"; Filename: "{app}\MusX Space.exe"
Name: "{autoprograms}\MusX Space"; Filename: "{app}\MusX Space.exe"
