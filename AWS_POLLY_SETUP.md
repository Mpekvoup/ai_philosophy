# 🚀 Настройка AWS Polly для AI-Философа

## Преимущества AWS Polly

✅ **Стабильность** - 99.9% uptime, официальный AWS сервис  
✅ **Качество** - Нейронные голоса высочайшего качества  
✅ **Надежность** - Нет ошибок 403, блокировок  
✅ **Профессиональность** - Используется в продакшене крупных компаний  
✅ **Масштабирование** - Поддерживает миллионы запросов  

## 📋 Требования

- AWS аккаунт (бесплатная регистрация)
- IAM пользователь с доступом к Polly
- AWS Access Key и Secret Key

---

## 🔧 Шаг 1: Создание AWS аккаунта

1. Перейдите на https://aws.amazon.com/
2. Нажмите "Create an AWS Account"
3. Заполните данные:
   - Email
   - Пароль
   - Имя аккаунта
4. Подтвердите кредитную карту (не спишут, нужно для верификации)
5. Выберите **Free Tier** план

**Free Tier включает:**
- 5 миллионов символов в месяц (Neural TTS)
- 12 месяцев бесплатно
- Для AI-Философа: **~10,000 запросов/месяц бесплатно**

---

## 🔑 Шаг 2: Создание IAM пользователя

### 2.1 Войдите в AWS Console

https://console.aws.amazon.com/

### 2.2 Откройте IAM

1. В поиске введите "IAM"
2. Откройте "IAM Dashboard"

### 2.3 Создайте пользователя

1. Нажмите "Users" → "Create user"
2. Имя: `ai-philosopher-polly`
3. Выберите: **Access key - Programmatic access**
4. Нажмите "Next"

### 2.4 Назначьте права

1. Выберите "Attach policies directly"
2. Найдите и выберите: **AmazonPollyFullAccess**
3. Нажмите "Next" → "Create user"

### 2.5 Получите ключи

**ВАЖНО:** Сохраните эти ключи сейчас, они больше не будут показаны!

1. После создания нажмите "Create access key"
2. Выберите "Application running outside AWS"
3. Скопируйте:
   - **Access Key ID** (например: `AKIAIOSFODNN7EXAMPLE`)
   - **Secret Access Key** (например: `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`)

---

## ⚙️ Шаг 3: Настройка проекта

### 3.1 Обновите зависимости

```bash
# Активируйте виртуальное окружение
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Установите boto3
pip install -r requirements.txt
```

### 3.2 Добавьте credentials в .env

Создайте/обновите файл `.env`:

```bash
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_key_here

# AWS Polly Credentials
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
AWS_POLLY_REGION=us-east-1

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Важные настройки:**

- `AWS_POLLY_REGION` - выберите ближайший регион:
  - `us-east-1` (США, Вирджиния) - рекомендуется
  - `eu-west-1` (Ирландия)
  - `ap-southeast-1` (Сингапур)

---

## ✅ Шаг 4: Тестирование

### 4.1 Запустите тестовый скрипт

```bash
python test_polly.py
```

**Ожидаемый вывод:**

```
🔊 Тестирование AWS Polly...
📦 Версия boto3: 1.34.34
✅ AWS credentials загружены
📍 Регион: us-east-1
🎤 Голос: Tatyana
📝 Текст: Привет! Это тестовое сообщение...
⏳ Генерация аудио...
✅ Успешно! Аудио сохранено в test_polly_audio.mp3
📊 Размер файла: 15234 байт
🎧 Прослушайте файл для проверки качества.

🗣️  Доступные русские Neural голоса:
--------------------------------------------------
  • Tatyana (Female)
  • Maxim (Male)

Всего голосов: 2
```

### 4.2 Прослушайте аудио

```bash
# Linux
xdg-open test_polly_audio.mp3

# Mac
open test_polly_audio.mp3

# Windows
start test_polly_audio.mp3
```

Если слышите естественную русскую речь - все работает! ✅

---

## 🚀 Шаг 5: Запуск приложения

```bash
# Примените миграции (если нужно)
python manage.py migrate

# Запустите сервер
python manage.py runserver
```

Откройте http://localhost:8000 и протестируйте голосовой ввод!

---

## 🐛 Устранение проблем

### Ошибка: "InvalidSignatureException"

**Причина:** Неверные AWS credentials

**Решение:**
1. Проверьте правильность `AWS_ACCESS_KEY_ID` и `AWS_SECRET_ACCESS_KEY` в .env
2. Убедитесь, что нет лишних пробелов
3. Создайте новые ключи в IAM если потеряли старые

### Ошибка: "AccessDeniedException"

**Причина:** IAM пользователь не имеет доступа к Polly

**Решение:**
1. Откройте IAM Console
2. Найдите пользователя
3. Добавьте политику **AmazonPollyFullAccess**

### Ошибка: "ThrottlingException"

**Причина:** Превышен лимит запросов

**Решение:**
1. Подождите несколько секунд между запросами
2. Free tier: до 5M символов/месяц
3. После free tier: ~$4 за 1M символов

### Не работает голос "Tatyana" или "Maxim"

**Причина:** Регион не поддерживает Neural voices

**Решение:**
1. Измените `AWS_POLLY_REGION=us-east-1` в .env
2. Перезапустите сервер
3. us-east-1 гарантированно поддерживает Neural

### Аудио есть, но не воспроизводится

**Причина:** Проблема с браузером

**Решение:**
1. Откройте консоль браузера (F12)
2. Проверьте ошибки JavaScript
3. Попробуйте другой браузер (Chrome/Edge)

---

## 💰 Стоимость

### Free Tier (первые 12 месяцев)
- **5 миллионов символов в месяц** - бесплатно
- Для AI-Философа: **~10,000 вопросов/месяц**

### После Free Tier
- **$4.00 за 1 миллион символов** (Neural TTS)

**Пример расчета:**

| Запросов/день | Символов на ответ | Месяц (30 дней) | Стоимость |
|---------------|-------------------|-----------------|-----------|
| 50            | 200               | 300,000         | $1.20     |
| 100           | 200               | 600,000         | $2.40     |
| 500           | 200               | 3,000,000       | $12.00    |

**Вывод:** Очень дешево! 🎉

---

## 📊 Мониторинг использования

### Проверить текущее использование:

1. Откройте AWS Console
2. Перейдите в "Billing Dashboard"
3. Нажмите "Free Tier"
4. Найдите "Amazon Polly"
5. Смотрите использование в реальном времени

### Настроить оповещения:

1. Billing Dashboard → "Budgets"
2. Create budget
3. Установите лимит (например $5/месяц)
4. Получайте email при превышении

---

## 🔒 Безопасность

### ⚠️ Не публикуйте credentials!

**Никогда не коммитьте:**
- `.env` файл
- AWS Access Keys в коде
- Любые секретные ключи

**Добавьте в .gitignore:**
```
.env
.env.local
*.pem
*.key
```

### Ротация ключей

Рекомендуется менять AWS ключи каждые 90 дней:

1. IAM Console → Users → `ai-philosopher-polly`
2. Security credentials
3. "Create access key"
4. Обновите .env
5. "Delete" старый ключ

---

## 🎯 Следующие шаги

✅ Настроили AWS Polly  
✅ Протестировали работу  
✅ Запустили приложение  

**Готово!** Теперь у вас стабильное, профессиональное TTS решение!

---

## 📚 Полезные ссылки

- [AWS Polly Documentation](https://docs.aws.amazon.com/polly/)
- [AWS Free Tier](https://aws.amazon.com/free/)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Polly Pricing](https://aws.amazon.com/polly/pricing/)
