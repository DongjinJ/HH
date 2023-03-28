@echo off

set /p str=FileName:
echo FileName - Create BBTAuto%str%.exe

python.exe -m pip install --upgrade pip
pip install Pyqt5
pip install psutil
pip install pyinstaller

pyinstaller -w -F BBTAuto.py

cd dist
ren "BBTAuto.exe" "BBTAuto_"%str%".exe"

pause