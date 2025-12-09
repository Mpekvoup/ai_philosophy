"""
Google Gemini API клиент для философских размышлений.
"""
import google.generativeai as genai
from django.conf import settings


class PhilosopherAI:
    """Класс для работы с Google Gemini API в роли AI-философа."""
    
    def __init__(self):
        """Инициализация клиента Gemini."""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY не установлен в переменных окружения")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Системный промпт для философа
        self.system_prompt = """Ты - мудрый AI-философ, который размышляет над глубокими вопросами бытия, 
        этики, познания и смысла жизни. Твои ответы должны быть:
        
        1. Глубокими и вдумчивыми
        2. Основанными на известных философских концепциях
        3. Понятными для широкой аудитории
        4. Краткими (2-4 предложения)
        5. Вдохновляющими и провоцирующими на размышления
        
        Отвечай на русском языке. Используй философские термины, но объясняй их простыми словами.
        Ссылайся на известных философов, когда это уместно (Сократ, Платон, Кант, Ницше, и др.).
        """
    
    def get_philosophical_response(self, user_question: str) -> str:
        """
        Получить философский ответ на вопрос пользователя.
        
        Args:
            user_question: Вопрос пользователя
            
        Returns:
            Философский ответ от Gemini
        """
        try:
            # Формируем полный промпт
            full_prompt = f"{self.system_prompt}\n\nВопрос: {user_question}\n\nОтвет:"
            
            # Генерируем ответ
            response = self.model.generate_content(full_prompt)
            
            return response.text
            
        except Exception as e:
            return f"Извините, произошла ошибка при размышлении: {str(e)}"
