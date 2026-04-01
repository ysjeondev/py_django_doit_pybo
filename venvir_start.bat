chcp 65001 > nul
@echo off
cd /d C:\pyDjango

echo ============================
echo 가상환경 진입 시작
echo ============================

call venvs\mysite\Scripts\activate

echo ============================
echo 가상환경 진입 완료
echo ============================

cmd