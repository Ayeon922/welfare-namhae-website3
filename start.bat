@echo off
chcp 65001
cls

echo.
echo ========================================
echo    노인 복지 추천 플랫폼
echo ========================================
echo.

:: Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [오류] Python이 설치되지 않았습니다.
    echo.
    echo Python 설치 방법:
    echo 1. Microsoft Store에서 "Python" 검색 후 설치
    echo 2. 또는 python.org에서 다운로드
    echo.
    pause
    exit /b 1
)

echo [정보] Python 버전 확인 중...
python --version

:: 패키지 설치 확인
echo.
echo [정보] 필요한 패키지를 설치하고 있습니다...
pip install -r requirements.txt

if errorlevel 1 (
    echo [오류] 패키지 설치에 실패했습니다.
    echo.
    echo 해결 방법:
    echo 1. 인터넷 연결을 확인하세요
    echo 2. pip를 업그레이드하세요: python -m pip install --upgrade pip
    echo 3. 다시 시도하세요
    echo.
    pause
    exit /b 1
)

:: 애플리케이션 실행
echo.
echo [정보] 애플리케이션을 시작합니다...
echo [정보] 브라우저에서 http://localhost:5000 으로 접속하세요
echo [정보] 종료하려면 Ctrl+C를 누르세요
echo.

python app.py

echo.
echo [정보] 애플리케이션이 종료되었습니다.
pause 