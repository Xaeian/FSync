py -m pip show pyinstaller > nul 2>&1 ^
  || py -m pip install -U pyinstaller

if exist .\dist\pyfsync.exe ^
  del .\dist\pyfsync.exe

py -m PyInstaller --onefile ^
  --workpath ./.build ^
  --distpath ./.dist ^
  --name pyfsync ^
  --icon=fsync.ico ^
  dist.py