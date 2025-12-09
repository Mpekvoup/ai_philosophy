#!/bin/bash

echo "🧠 AI-Философ - Установка"
echo "========================="
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.8 или выше."
    exit 1
fi

echo "✅ Python найден: $(python3 --version)"
echo ""

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Проверка .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден. Создание из .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  ВАЖНО: Отредактируйте файл .env и добавьте ваш GEMINI_API_KEY"
    echo "   Получить ключ можно здесь: https://makersuite.google.com/app/apikey"
    echo ""
fi

# Миграции базы данных
echo "🗄️  Применение миграций базы данных..."
python manage.py migrate

echo ""
echo "✅ Установка завершена!"
echo ""
echo "🚀 Для запуска сервера выполните:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "📝 Не забудьте добавить GEMINI_API_KEY в файл .env"
