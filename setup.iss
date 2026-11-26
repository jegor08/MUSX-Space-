[Setup]
AppName=MusX Space Alpha
AppVersion=2.0-alpha1
DefaultDirName={localappdata}\MusX Space Alpha
PrivilegesRequired=lowest
OutputDir=output
OutputBaseFilename=MusX_Space_Alpha_Setup
SetupIconFile=musx.ico
[Files]
Source: "dist\MusX Space.exe"; DestDir: "{app}"; Flags: ignoreversion
[Icons]
Name: "{autodesktop}\MusX Space Alpha"; Filename: "{app}\MusX Space.exe"
Name: "{autoprograms}\MusX Space Alpha"; Filename: "{app}\MusX Space.exe"
