py -m pip show pyinstaller > nul 2>&1 ^
  || py -m pip install -U pyinstaller

if exist .\dist\FSync.exe ^
  del .\dist\FSync.exe

pyinstaller --onefile ^
  --workpath ./.build ^
  --distpath ./.dist ^
  --name FSync ^
  --icon=fsync.ico ^
  --paths=./dev_console ^
  dist.py