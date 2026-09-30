@echo off
python -m pip install --upgrade pyinstaller
python -m PyInstaller --noconfirm --clean --windowed --name AttendanceSystem --add-data "view;view" --add-data "assets;assets" main.py
pause
