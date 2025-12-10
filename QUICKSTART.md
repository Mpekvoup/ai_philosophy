# 🚀 Быстрый старт AI-Философа

Следуйте этим шагам для запуска приложения:

## 1️⃣ Установка Python пакетов

```bash
# Создайте виртуальное окружение
python -m venv venv

# Активируйте его
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установите зависимости (включая boto3 для AWS Polly)
pip install -r requirements.txt
```

## 2️⃣ Настройка API ключей

### Google Gemini API:
1. Перейдите на https://makersuite.google.com/app/apikey
2. Войдите с Google аккаунтом
3. Создайте новый API ключ

### AWS Polly (для озвучивания):
**Подробная инструкция:** см. [AWS_POLLY_SETUP.md](AWS_POLLY_SETUP.md)

Кратко:
1. Создайте AWS аккаунт (бесплатно)
2. Создайте IAM пользователя с правами Polly
3. Получите Access Key и Secret Key

### Создайте файл `.env`:
```bash
cp .env.example .env
```

### Заполните `.env`:
```env
GEMINI_API_KEY=your_gemini_key_here

AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_POLLY_REGION=us-east-1
```

## 3️⃣ Инициализация базы данных

```bash
python manage.py migrate
```

## 4️⃣ Запуск сервера

```bash
python manage.py runserver
```

## 5️⃣ Открытие приложения

Откройте в браузере (Chrome или Edge):
```
http://localhost:8000
```

## 6️⃣ Тестирование AWS Polly (ВАЖНО!)

Перед запуском приложения протестируйте AWS Polly:

```bash
python test_polly.py
```

Должно вывести:
```
✅ AWS Polly работает корректно!
```

Если ошибка - см. [AWS_POLLY_SETUP.md](AWS_POLLY_SETUP.md)

## 7️⃣ Использование

1. Нажмите кнопку микрофона
2. Разрешите доступ к микрофону
3. Задайте философский вопрос голосом
4. Получите мудрый ответ в текстовом виде
5. Автоматически воспроизведется озвучка через AWS Polly
6. Используйте кнопки в истории для повторного прослушивания

---

## ⚠️ Важно

- **Браузер**: Используйте Chrome или Edge (Safari не поддерживается)
- **Микрофон**: Разрешите доступ при первом запуске
- **API ключи**: Обязательно добавьте Gemini + AWS в .env
- **Озвучивание**: AWS Polly (99.9% uptime, стабильно)
- **Звук**: Проверьте, что звук включен в браузере и системе

## 🆘 Проблемы?

### AWS Polly не работает?
```bash
# Проверьте credentials
python test_polly.py

# Если ошибка - см. детальную инструкцию
```

### Подробное устранение неполадок:
- Настройка AWS Polly: см. [AWS_POLLY_SETUP.md](AWS_POLLY_SETUP.md)
- Общие проблемы: см. README.md раздел "Решение проблем"
