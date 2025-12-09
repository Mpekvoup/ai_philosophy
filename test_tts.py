#!/usr/bin/env python
"""
Скрипт для тестирования Edge-TTS.
Запустите: python test_tts.py
"""
import asyncio
import sys

try:
    import edge_tts
except ImportError:
    print("❌ edge-tts не установлен!")
    print("Установите: pip install --upgrade edge-tts")
    sys.exit(1)


async def test_edge_tts():
    """Тестирование Edge-TTS с русским голосом."""
    print("🔊 Тестирование Edge-TTS...")
    print(f"📦 Версия edge-tts: {edge_tts.__version__}")
    print()
    
    text = "Привет! Это тестовое сообщение от AI-Философа."
    voice = "ru-RU-SvetlanaNeural"
    output_file = "test_audio.mp3"
    
    try:
        print(f"🎤 Голос: {voice}")
        print(f"📝 Текст: {text}")
        print("⏳ Генерация аудио...")
        
        communicate = edge_tts.Communicate(
            text,
            voice,
            rate="+0%",
            volume="+0%",
            pitch="+0Hz"
        )
        
        # Сохраняем в файл
        await communicate.save(output_file)
        
        print(f"✅ Успешно! Аудио сохранено в {output_file}")
        print()
        print("🎧 Прослушайте файл для проверки качества.")
        print("💡 Если вы слышите речь - Edge-TTS работает корректно!")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        print()
        print("🔍 Возможные причины:")
        print("1. Нет подключения к интернету")
        print("2. Microsoft API недоступен")
        print("3. Устаревшая версия edge-tts")
        print()
        print("💡 Решения:")
        print("- Проверьте интернет: ping speech.platform.bing.com")
        print("- Обновите edge-tts: pip install --upgrade edge-tts")
        print("- Попробуйте VPN")
        print("- См. TROUBLESHOOTING_TTS.md для деталей")
        
        return False


async def list_russian_voices():
    """Список доступных русских голосов."""
    print("\n🗣️  Доступные русские голоса:")
    print("-" * 50)
    
    try:
        voices = await edge_tts.list_voices()
        russian_voices = [v for v in voices if v['Locale'].startswith('ru-')]
        
        for voice in russian_voices:
            name = voice['ShortName']
            gender = voice['Gender']
            print(f"  • {name} ({gender})")
            
        print(f"\nВсего голосов: {len(russian_voices)}")
        
    except Exception as e:
        print(f"❌ Не удалось получить список голосов: {str(e)}")


def main():
    """Главная функция."""
    print("=" * 60)
    print("  AI-Философ - Тест Edge-TTS")
    print("=" * 60)
    print()
    
    # Запускаем тест
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        success = loop.run_until_complete(test_edge_tts())
        
        if success:
            # Показываем доступные голоса
            loop.run_until_complete(list_russian_voices())
            
        print()
        print("=" * 60)
        
        if success:
            print("✅ Edge-TTS работает корректно!")
            sys.exit(0)
        else:
            print("❌ Edge-TTS не работает. См. ошибки выше.")
            sys.exit(1)
            
    finally:
        loop.close()


if __name__ == "__main__":
    main()
