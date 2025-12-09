# 🔊 Решение проблем с Edge-TTS

## Ошибка 403 при генерации аудио

Если вы видите ошибку:
```
403, message='Invalid response status', url='wss://speech.platform.bing.com/...'
```

### Решение 1: Обновите edge-tts

```bash
# Активируйте виртуальное окружение
source venv/bin/activate  # Linux/Mac
# или venv\Scripts\activate  # Windows

# Обновите edge-tts до последней версии
pip install --upgrade edge-tts

# Проверьте версию
pip show edge-tts
```

Должна быть версия **6.1.12 или выше**.

### Решение 2: Переустановите зависимости

```bash
# Удалите старые зависимости
pip uninstall edge-tts -y

# Переустановите
pip install -r requirements.txt
```

### Решение 3: Проверьте подключение к интернету

Edge-TTS требует подключения к Microsoft API:
```bash
# Проверьте доступность
ping speech.platform.bing.com
```

### Решение 4: Используйте VPN

Microsoft может блокировать запросы из некоторых регионов. Попробуйте:
1. Включить VPN (USA, Europe)
2. Перезапустить Django сервер

## Тестирование Edge-TTS

Проверьте работу Edge-TTS напрямую:

```python
import asyncio
import edge_tts

async def test_tts():
    text = "Привет, это тест"
    voice = "ru-RU-SvetlanaNeural"
    
    communicate = edge_tts.Communicate(text, voice)
    
    await communicate.save("test.mp3")
    print("✅ Аудио сохранено в test.mp3")

# Запустите
asyncio.run(test_tts())
```

Если этот код работает, проблема в интеграции с Django.

## Альтернативные голоса

Попробуйте другие русские голоса:

```python
# В tts_client.py измените:
RUSSIAN_VOICES = {
    'female': 'ru-RU-DariyaNeural',  # Альтернативный женский
    'male': 'ru-RU-DmitryNeural',    # Мужской
}
```

Список всех голосов:
```bash
edge-tts --list-voices | grep ru-RU
```

## Проверка логов Django

Включите детальное логирование:

```python
# В settings.py добавьте:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

Перезапустите сервер и проверьте вывод.

## Известные проблемы

### 1. Проблемы с asyncio в Django

**Симптом:** Ошибки event loop

**Решение:** Код уже исправлен - создается новый event loop для каждого запроса.

### 2. Timeout

**Симптом:** Запрос зависает

**Решение:** Увеличьте timeout в views.py:
```python
# В ask_philosopher добавьте:
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("TTS timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 секунд

try:
    audio_bytes = tts_client.generate_audio(answer)
finally:
    signal.alarm(0)  # Отключаем таймер
```

### 3. Большие тексты

**Симптом:** Ошибка генерации для длинных ответов

**Решение:** Ограничьте длину текста:
```python
# В gemini_client.py измените промпт:
"4. Краткими (2-3 предложения максимум)"
```

## Статус Microsoft API

Проверьте статус API:
- https://status.azure.com/
- https://downdetector.com/status/microsoft/

Если API Microsoft недоступен, попробуйте позже.

## Контакты для помощи

Если проблема сохраняется:
1. Проверьте issues на GitHub: https://github.com/rany2/edge-tts/issues
2. Создайте новый issue с логами и версией edge-tts
3. Укажите вашу ОС и версию Python

## Альтернативный TTS (если Edge-TTS не работает)

Если Edge-TTS не работает, можно использовать gTTS:

```bash
pip install gTTS
```

Замените в tts_client.py:
```python
from gtts import gTTS
import io

def generate_audio(self, text: str) -> bytes:
    tts = gTTS(text=text, lang='ru')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp.read()
```

**Минусы gTTS:**
- Требует Google API (может блокироваться)
- Менее естественный голос
- Медленнее
