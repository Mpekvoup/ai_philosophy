"""
Views для AI-философа.
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .gemini_client import PhilosopherAI


def index(request):
    """Главная страница приложения."""
    return render(request, 'index.html')


@csrf_exempt
@require_http_methods(["POST"])
def ask_philosopher(request):
    """
    API endpoint для получения философского ответа.
    
    Принимает JSON с полем 'question' и возвращает философский ответ.
    """
    try:
        # Парсим JSON из запроса
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        
        if not question:
            return JsonResponse({
                'error': 'Вопрос не может быть пустым'
            }, status=400)
        
        # Создаем экземпляр AI-философа и получаем ответ
        philosopher = PhilosopherAI()
        answer = philosopher.get_philosophical_response(question)
        
        return JsonResponse({
            'question': question,
            'answer': answer
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Неверный формат JSON'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка сервера: {str(e)}'
        }, status=500)
