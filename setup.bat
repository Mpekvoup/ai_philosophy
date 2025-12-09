@echo off
echo 🧠 AI-Философ - Установка
echo =========================
echo.

REM Проверка Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден. Установите Python 3.8 или выше.
    pause
    exit /b 1
)

echo ✅ Python найден
python --version
echo.

REM Создание виртуального окружения
echo 📦 Создание виртуального окружения...
python -m venv venv

REM Активация виртуального окружения
echo 🔧 Активация виртуального окружения...
call venv\Scripts\activate.bat

REM Установка зависимостей
echo 📥 Установка зависимостей...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Проверка .env файла
if not exist .env (
    echo ⚠️  Файл .env не найден. Создание из .env.example...
    copy .env.example .env
    echo.
    echo ⚠️  ВАЖНО: Отредактируйте файл .env и добавьте ваш GEMINI_API_KEY
    echo    Получить ключ можно здесь: https://makersuite.google.com/app/apikey
    echo.
)

REM Миграции базы данных
echo 🗄️  Применение миграций базы данных...
python manage.py migrate

echo.
echo ✅ Установка завершена!
echo.
echo 🚀 Для запуска сервера выполните:
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 📝 Не забудьте добавить GEMINI_API_KEY в файл .env
echo.
pause
