"""
Views для AI-философа.
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import base64
import logging

from .gemini_client import PhilosopherAI
from .polly_client import PollyTTSClient

logger = logging.getLogger(__name__)


def index(request):
    """Главная страница приложения."""
    return render(request, 'index.html')


@csrf_exempt
@require_http_methods(["POST"])
def ask_philosopher(request):
    """
    API endpoint для получения философского ответа с озвучиванием.

    Принимает JSON с полем 'question' и возвращает:
    - Текстовый ответ
    - Аудио в формате base64 (MP3)
    """
    try:
        # Парсим JSON из запроса
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        voice = data.get('voice', 'female')  # По умолчанию женский голос

        if not question:
            return JsonResponse({
                'error': 'Вопрос не может быть пустым'
            }, status=400)

        logger.info(f"Получен вопрос: {question}")

        # Создаем экземпляр AI-философа и получаем ответ
        philosopher = PhilosopherAI()
        answer = philosopher.get_philosophical_response(question)

        logger.info(f"Получен ответ от Gemini: {answer[:100]}...")

        # Генерируем аудио из ответа через AWS Polly
        try:
            tts_client = PollyTTSClient(voice=voice)
            audio_bytes = tts_client.generate_audio(answer)

            # Кодируем аудио в base64 для передачи в JSON
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

            logger.info(f"Сгенерировано аудио: {len(audio_bytes)} байт")

            return JsonResponse({
                'question': question,
                'answer': answer,
                'audio': audio_base64,
                'audio_format': 'mp3'
            })

        except Exception as tts_error:
            # Если TTS не удалось, возвращаем хотя бы текст
            logger.error(f"Ошибка генерации аудио: {str(tts_error)}")
            return JsonResponse({
                'question': question,
                'answer': answer,
                'error': f'Не удалось сгенерировать аудио: {str(tts_error)}'
            })

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Неверный формат JSON'
        }, status=400)

    except Exception as e:
        logger.error(f"Ошибка сервера: {str(e)}")
        return JsonResponse({
            'error': f'Ошибка сервера: {str(e)}'
        }, status=500)
