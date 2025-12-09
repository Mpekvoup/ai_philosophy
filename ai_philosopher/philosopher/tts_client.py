"""
Edge-TTS клиент для озвучивания текста.
Microsoft Edge Text-to-Speech - бесплатный высококачественный TTS.
"""
import edge_tts
import asyncio
import io
import logging

logger = logging.getLogger(__name__)


class TextToSpeechClient:
    """Класс для генерации речи из текста через Edge-TTS."""
    
    # Лучшие русские голоса Microsoft Edge TTS
    RUSSIAN_VOICES = {
        'female': 'ru-RU-SvetlanaNeural',  # Женский голос (естественный)
        'male': 'ru-RU-DmitryNeural',      # Мужской голос (естественный)
    }
    
    def __init__(self, voice='female'):
        """
        Инициализация TTS клиента.
        
        Args:
            voice: 'female' или 'male'
        """
        self.voice = self.RUSSIAN_VOICES.get(voice, self.RUSSIAN_VOICES['female'])
        logger.info(f"Инициализирован TTS с голосом: {self.voice}")
    
    async def generate_audio_async(self, text: str) -> bytes:
        """
        Асинхронная генерация аудио из текста.
        
        Args:
            text: Текст для озвучивания
            
        Returns:
            bytes: MP3 аудио данные
        """
        try:
            # Создаем коммуникатор Edge-TTS
            communicate = edge_tts.Communicate(text, self.voice)
            
            # Генерируем аудио в память
            audio_data = io.BytesIO()
            
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data.write(chunk["data"])
            
            # Возвращаем аудио данные
            audio_bytes = audio_data.getvalue()
            logger.info(f"Сгенерировано аудио: {len(audio_bytes)} байт")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Ошибка при генерации аудио: {str(e)}")
            raise
    
    def generate_audio(self, text: str) -> bytes:
        """
        Синхронная обертка для генерации аудио.
        
        Args:
            text: Текст для озвучивания
            
        Returns:
            bytes: MP3 аудио данные
        """
        try:
            # Создаем новый event loop если его нет
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Запускаем асинхронную функцию
            return loop.run_until_complete(self.generate_audio_async(text))
            
        except Exception as e:
            logger.error(f"Ошибка в синхронной генерации аудио: {str(e)}")
            raise
    
    @staticmethod
    async def list_available_voices():
        """
        Получить список доступных голосов.
        
        Returns:
            list: Список доступных голосов
        """
        voices = await edge_tts.list_voices()
        # Фильтруем только русские голоса
        russian_voices = [v for v in voices if v['Locale'].startswith('ru-')]
        return russian_voices
