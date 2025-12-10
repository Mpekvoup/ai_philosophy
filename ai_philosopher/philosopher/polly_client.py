"""
AWS Polly клиент для озвучивания текста.
Amazon Polly - профессиональный нейронный TTS.
"""
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class PollyTTSClient:
    """Класс для генерации речи из текста через AWS Polly."""
    
    # Лучшие русские нейронные голоса AWS Polly
    RUSSIAN_VOICES = {
        'female': 'Tatyana',  # Женский голос (Neural)
        'male': 'Maxim',      # Мужской голос (Neural)
    }
    
    def __init__(self, voice='female'):
        """
        Инициализация AWS Polly клиента.
        
        Args:
            voice: 'female' или 'male'
        """
        self.voice_id = self.RUSSIAN_VOICES.get(voice, self.RUSSIAN_VOICES['female'])
        self.region = settings.AWS_POLLY_REGION
        
        # Создаем клиента AWS Polly
        try:
            self.polly_client = boto3.client(
                'polly',
                region_name=self.region,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            logger.info(f"Инициализирован AWS Polly с голосом: {self.voice_id}, регион: {self.region}")
        except Exception as e:
            logger.error(f"Ошибка инициализации AWS Polly: {str(e)}")
            raise
    
    def generate_audio(self, text: str, max_retries: int = 3) -> bytes:
        """
        Генерация аудио из текста с повторными попытками.
        
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
                
                # Вызываем AWS Polly synthesize_speech
                response = self.polly_client.synthesize_speech(
                    Text=text,
                    OutputFormat='mp3',
                    VoiceId=self.voice_id,
                    Engine='neural',  # Используем нейронный движок
                    LanguageCode='ru-RU'
                )
                
                # Читаем аудио из потока
                if 'AudioStream' in response:
                    audio_bytes = response['AudioStream'].read()
                    
                    if len(audio_bytes) == 0:
                        raise ValueError("Получены пустые аудио данные от AWS Polly")
                    
                    logger.info(f"Успешно сгенерировано аудио: {len(audio_bytes)} байт")
                    return audio_bytes
                else:
                    raise ValueError("AWS Polly не вернул аудио поток")
                    
            except (BotoCoreError, ClientError) as boto_error:
                last_error = boto_error
                logger.warning(f"Попытка {attempt + 1} неудачна (AWS error): {str(boto_error)}")
                
                # Если это ошибка аутентификации, не повторяем
                if 'InvalidSignature' in str(boto_error) or 'AccessDenied' in str(boto_error):
                    raise
                    
            except Exception as e:
                last_error = e
                logger.warning(f"Попытка {attempt + 1} неудачна: {str(e)}")
        
        # Если все попытки исчерпаны
        error_msg = f"Не удалось сгенерировать аудио после {max_retries} попыток: {str(last_error)}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    @staticmethod
    def list_available_voices(region='us-east-1'):
        """
        Получить список доступных голосов.
        
        Args:
            region: AWS регион
            
        Returns:
            list: Список доступных русских голосов
        """
        try:
            # Временный клиент для получения голосов
            temp_client = boto3.client('polly', region_name=region)
            
            response = temp_client.describe_voices(
                Engine='neural',
                LanguageCode='ru-RU'
            )
            
            return response.get('Voices', [])
            
        except Exception as e:
            logger.error(f"Ошибка получения списка голосов: {str(e)}")
            return []
