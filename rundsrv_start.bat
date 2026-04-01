@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8

cd /d C:\pyDjango\projects\projectmysite

echo ============================
echo Django 서버 시작
echo ============================

python manage.py runserver 0.0.0.0:8000

pause