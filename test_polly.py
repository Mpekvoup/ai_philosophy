#!/usr/bin/env python
"""
Скрипт для тестирования AWS Polly.
Запустите: python test_polly.py
"""
import sys
import os

# Добавляем путь к Django проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Загружаем .env
from dotenv import load_dotenv
load_dotenv()

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    print("❌ boto3 не установлен!")
    print("Установите: pip install boto3")
    sys.exit(1)


def test_aws_polly():
    """Тестирование AWS Polly с русским голосом."""
    print("🔊 Тестирование AWS Polly...")
    print(f"📦 Версия boto3: {boto3.__version__}")
    print()
    
    # Получаем credentials из env
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_POLLY_REGION', 'us-east-1')
    
    if not access_key or not secret_key:
        print("❌ AWS credentials не найдены в .env!")
        print()
        print("Добавьте в .env:")
        print("AWS_ACCESS_KEY_ID=your_key_here")
        print("AWS_SECRET_ACCESS_KEY=your_secret_here")
        print("AWS_POLLY_REGION=us-east-1")
        return False
    
    print(f"✅ AWS credentials загружены")
    print(f"📍 Регион: {region}")
    print()
    
    text = "Привет! Это тестовое сообщение от AI-Философа через AWS Polly."
    voice_id = "Tatyana"  # Женский русский голос
    output_file = "test_polly_audio.mp3"
    
    try:
        print(f"🎤 Голос: {voice_id}")
        print(f"📝 Текст: {text}")
        print("⏳ Генерация аудио...")
        
        # Создаем клиента Polly
        polly_client = boto3.client(
            'polly',
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        
        # Генерируем речь
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice_id,
            Engine='standard',  # Русские голоса поддерживают только standard
            LanguageCode='ru-RU'
        )
        
        # Сохраняем в файл
        if 'AudioStream' in response:
            with open(output_file, 'wb') as file:
                file.write(response['AudioStream'].read())
            
            file_size = os.path.getsize(output_file)
            print(f"✅ Успешно! Аудио сохранено в {output_file}")
            print(f"📊 Размер файла: {file_size} байт")
            print()
            print("🎧 Прослушайте файл для проверки качества.")
            print("💡 Если вы слышите речь - AWS Polly работает корректно!")
            
            # Показываем доступные голоса
            list_russian_voices(polly_client)
            
            return True
        else:
            print("❌ Не удалось получить аудио поток от AWS Polly")
            return False
        
    except ClientError as e:
        print(f"❌ Ошибка AWS Polly: {e}")
        print()
        print("🔍 Возможные причины:")
        print("1. Неверные AWS credentials")
        print("2. Нет доступа к Polly в IAM")
        print("3. Регион не поддерживает выбранный голос")
        print("4. Превышена квота free tier")
        print()
        print("💡 Решения:")
        print("- Проверьте credentials в .env")
        print("- Проверьте IAM права (AmazonPollyFullAccess)")
        print("- Попробуйте другой регион (us-east-1, eu-west-1)")
        print("- Проверьте AWS console для статуса аккаунта")
        
        return False
        
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False


def list_russian_voices(polly_client):
    """Список доступных русских голосов."""
    print("\n🗣️  Доступные русские голоса:")
    print("-" * 50)

    try:
        response = polly_client.describe_voices(
            Engine='standard',
            LanguageCode='ru-RU'
        )
        
        voices = response.get('Voices', [])
        
        for voice in voices:
            name = voice['Id']
            gender = voice['Gender']
            print(f"  • {name} ({gender})")
        
        print(f"\nВсего голосов: {len(voices)}")
        
    except Exception as e:
        print(f"❌ Не удалось получить список голосов: {str(e)}")


def main():
    """Главная функция."""
    print("=" * 60)
    print("  AI-Философ - Тест AWS Polly")
    print("=" * 60)
    print()
    
    success = test_aws_polly()
    
    print()
    print("=" * 60)
    
    if success:
        print("✅ AWS Polly работает корректно!")
        sys.exit(0)
    else:
        print("❌ AWS Polly не работает. См. ошибки выше.")
        sys.exit(1)


if __name__ == "__main__":
    main()
