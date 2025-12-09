# 🧠 AI-Философ | Real-time Голосовой Помощник

Веб-приложение для философских размышлений с использованием голосового ввода и Google Gemini Cloud API.

## ✨ Особенности

- 🎤 **Real-time распознавание речи** через Web Speech API (встроен в Chrome/Edge)
- 💭 **AI-философ на базе Google Gemini** (gemini-1.5-flash)
- 🚀 **Без записи аудиофайлов** - только текстовая обработка
- 📜 **История диалога** - сохранение всех вопросов и ответов
- 🎨 **Современный UI** - адаптивный дизайн с темной темой

## 🏗️ Архитектура

```
Browser (Web Speech API) → Распознавание речи в ТЕКСТ
    ↓
JavaScript → POST запрос с текстом на Django
    ↓
Django Backend → Обработка текста
    ↓
Google Gemini Cloud API → Философский ответ
    ↓
Django → Возврат ответа в JSON
    ↓
JavaScript → Отображение ответа пользователю
```

## 📋 Требования

- Python 3.8+
- Django 5.0+
- Google Gemini API Key
- Браузер: Chrome или Edge (для Web Speech API)

## 🚀 Быстрый старт

### 1. Клонирование и установка зависимостей

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта:

```bash
cp .env.example .env
```

Отредактируйте `.env` и добавьте ваш Google Gemini API Key:

```env
# Google Gemini API Key
GEMINI_API_KEY=ваш_api_ключ_здесь

# Django Settings
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Получение Google Gemini API Key

1. Перейдите на [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Войдите с вашим Google аккаунтом
3. Создайте новый API ключ
4. Скопируйте ключ и вставьте в файл `.env`

### 4. Инициализация базы данных

```bash
python manage.py migrate
```

### 5. Создание суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: **http://localhost:8000**

## 🎯 Использование

1. Откройте приложение в **Chrome** или **Edge**
2. При первом запуске разрешите доступ к микрофону
3. Нажмите кнопку "Нажмите, чтобы говорить"
4. Задайте философский вопрос голосом (на русском языке)
5. Дождитесь ответа от AI-философа
6. Все диалоги сохраняются в истории

## 🎨 Примеры философских вопросов

- "В чем смысл жизни?"
- "Что такое счастье?"
- "Существует ли свобода воли?"
- "Что важнее: знание или мудрость?"
- "Можем ли мы познать истину?"

## 📁 Структура проекта

```
ai_philosophy/
├── ai_philosopher/                 # Главная директория проекта
│   ├── __init__.py
│   ├── settings.py                # Настройки Django
│   ├── urls.py                    # Главные URL маршруты
│   ├── wsgi.py
│   ├── asgi.py
│   ├── philosopher/               # Приложение философа
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── views.py              # Обработчики запросов
│   │   ├── urls.py               # URL маршруты приложения
│   │   └── gemini_client.py      # Интеграция с Gemini API
│   ├── static/                    # Статические файлы
│   │   ├── css/
│   │   │   └── style.css         # Стили интерфейса
│   │   └── js/
│   │       └── app.js            # Web Speech API логика
│   └── templates/
│       └── index.html            # Главная страница
├── manage.py                      # Django management команды
├── requirements.txt               # Python зависимости
├── .env.example                   # Пример файла окружения
└── README.md                      # Документация
```

## 🔧 Технологии

### Frontend
- **Web Speech API** - встроенное распознавание речи в браузере
- **Vanilla JavaScript** - без дополнительных фреймворков
- **CSS3** - современные стили и анимации

### Backend
- **Django 5.0** - Python веб-фреймворк
- **Google Generative AI** - интеграция с Gemini API
- **Python-dotenv** - управление переменными окружения

### AI
- **Google Gemini 1.5 Flash** - быстрая и эффективная языковая модель
- Специальный философский промпт для глубоких размышлений

## ⚙️ API Endpoints

### `GET /`
Главная страница приложения

### `POST /api/ask/`
Отправка вопроса философу

**Request:**
```json
{
  "question": "В чем смысл жизни?"
}
```

**Response:**
```json
{
  "question": "В чем смысл жизни?",
  "answer": "Философский ответ от Gemini..."
}
```

## 🐛 Решение проблем

### Микрофон не работает
- Проверьте разрешения для микрофона в настройках браузера
- Используйте Chrome или Edge (Safari не поддерживает Web Speech API)
- Убедитесь, что микрофон подключен и работает

### Ошибка API
- Проверьте правильность API ключа в файле `.env`
- Убедитесь, что API ключ активен в Google AI Studio
- Проверьте подключение к интернету

### Распознавание речи не работает
- Говорите четко и громко
- Проверьте, что выбран правильный язык (ru-RU)
- Убедитесь, что микрофон не заблокирован другими приложениями

## 📝 Настройка философского промпта

Чтобы изменить стиль ответов философа, отредактируйте `system_prompt` в файле:
```
ai_philosopher/philosopher/gemini_client.py
```

## 🔐 Безопасность

- Не публикуйте файл `.env` с API ключами в публичных репозиториях
- В продакшене используйте HTTPS
- Установите `DEBUG=False` в продакшене
- Используйте надежный `SECRET_KEY` для Django

## 📄 Лицензия

MIT License

## 👨‍💻 Автор

Created with ❤️ using Django + Google Gemini Cloud API

## 🤝 Вклад в проект

Pull requests приветствуются! Для крупных изменений сначала откройте issue.

---

**Powered by:**
- 🚀 Django 5.0
- 🧠 Google Gemini 1.5 Flash
- 🎤 Web Speech API
