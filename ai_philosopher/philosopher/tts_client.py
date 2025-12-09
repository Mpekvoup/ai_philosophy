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
    
    async def generate_audio_async(self, text: str, max_retries: int = 3) -> bytes:
        """
        Асинхронная генерация аудио из текста с повторными попытками.

        Args:
            text: Текст для озвучивания
            max_retries: Максимальное количество попыток

        Returns:
            bytes: MP3 аудио данные
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                logger.info(f"Попытка генерации аудио {attempt + 1}/{max_retries}")

                # Создаем коммуникатор Edge-TTS с настройками
                communicate = edge_tts.Communicate(
                    text,
                    self.voice,
                    rate="+0%",  # Нормальная скорость
                    volume="+0%",  # Нормальная громкость
                    pitch="+0Hz"  # Нормальная высота
                )

                # Генерируем аудио в память
                audio_data = io.BytesIO()

                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_data.write(chunk["data"])

                # Возвращаем аудио данные
                audio_bytes = audio_data.getvalue()

                if len(audio_bytes) == 0:
                    raise ValueError("Получены пустые аудио данные")

                logger.info(f"Успешно сгенерировано аудио: {len(audio_bytes)} байт")
                return audio_bytes

            except Exception as e:
                last_error = e
                logger.warning(f"Попытка {attempt + 1} неудачна: {str(e)}")

                # Ждем перед следующей попыткой
                if attempt < max_retries - 1:
                    await asyncio.sleep(1 * (attempt + 1))  # Экспоненциальная задержка

        # Если все попытки исчерпаны
        error_msg = f"Не удалось сгенерировать аудио после {max_retries} попыток: {str(last_error)}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    def generate_audio(self, text: str) -> bytes:
        """
        Синхронная обертка для генерации аудио.

        Args:
            text: Текст для озвучивания

        Returns:
            bytes: MP3 аудио данные
        """
        try:
            # ВАЖНО: Создаем НОВЫЙ event loop для каждого запроса
            # Это решает проблемы с закрытыми соединениями в Django
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                # Запускаем асинхронную функцию
                result = loop.run_until_complete(self.generate_audio_async(text))
                return result
            finally:
                # Закрываем loop после использования
                loop.close()

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
