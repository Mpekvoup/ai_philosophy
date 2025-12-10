// AI-Философ - Real-time голосовое взаимодействие

class PhilosopherApp {
    constructor() {
        this.recognition = null;
        this.isRecording = false;
        this.currentTranscript = '';
        this.currentAudio = null;  // Текущий аудио плеер
        this.currentAudioBlob = null;  // Текущий аудио blob для повтора
        this.noSpeechCount = 0;  // Счетчик ошибок no-speech
        this.maxNoSpeechRetries = 3;  // Максимум попыток перезапуска

        // DOM элементы
        this.recordBtn = document.getElementById('recordBtn');
        this.status = document.getElementById('status');
        this.transcript = document.getElementById('transcript');
        this.answer = document.getElementById('answer');
        this.loading = document.getElementById('loading');
        this.history = document.getElementById('history');
        this.audioControls = document.getElementById('audioControls');
        this.speakingAnimation = document.getElementById('speakingAnimation');

        this.init();
    }
    
    init() {
        // Проверяем поддержку Web Speech API
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.showError('Ваш браузер не поддерживает распознавание речи. Используйте Chrome или Edge.');
            this.recordBtn.disabled = true;
            return;
        }

        // Инициализируем распознавание речи
        this.setupSpeechRecognition();

        // Обработчик кнопки записи
        this.recordBtn.addEventListener('click', () => this.toggleRecording());

        // Обработчик кнопки повтора аудио
        const replayBtn = document.getElementById('replayBtn');
        if (replayBtn) {
            replayBtn.addEventListener('click', () => this.replayAudio());
        }

        console.log('AI-Философ инициализирован с поддержкой AWS Polly');
    }
    
    setupSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        // Настройки распознавания
        this.recognition.continuous = false;  // Остановка после паузы
        this.recognition.interimResults = true;  // Промежуточные результаты
        this.recognition.lang = 'ru-RU';  // Русский язык
        this.recognition.maxAlternatives = 1;
        
        // Обработчики событий
        this.recognition.onstart = () => this.onRecognitionStart();
        this.recognition.onresult = (event) => this.onRecognitionResult(event);
        this.recognition.onerror = (event) => this.onRecognitionError(event);
        this.recognition.onend = () => this.onRecognitionEnd();
    }
    
    toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            this.startRecording();
        }
    }
    
    startRecording() {
        try {
            this.recognition.start();
            this.isRecording = true;
            this.currentTranscript = '';
            this.noSpeechCount = 0;  // Сбрасываем счетчик

            // Обновляем UI
            this.recordBtn.classList.add('recording');
            this.recordBtn.querySelector('.btn-text').textContent = 'Говорите... (нажмите, чтобы остановить)';
            this.updateStatus('🎤 Слушаю...', 'listening');
            this.transcript.textContent = 'Говорите ваш вопрос...';

        } catch (error) {
            console.error('Ошибка при запуске записи:', error);
            this.showError('Не удалось запустить запись. Проверьте разрешения для микрофона.');
        }
    }
    
    stopRecording() {
        if (this.recognition && this.isRecording) {
            this.recognition.stop();
        }
    }
    
    onRecognitionStart() {
        console.log('Распознавание речи началось');
    }
    
    onRecognitionResult(event) {
        let interimTranscript = '';
        let finalTranscript = '';
        
        // Обрабатываем результаты
        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            } else {
                interimTranscript += transcript;
            }
        }
        
        // Обновляем отображение
        if (finalTranscript) {
            this.currentTranscript = finalTranscript;
            this.transcript.textContent = finalTranscript;
            
            // Отправляем вопрос на сервер
            this.sendQuestionToServer(finalTranscript);
            
        } else if (interimTranscript) {
            this.transcript.textContent = interimTranscript + '...';
        }
    }
    
    onRecognitionError(event) {
        console.log('Событие распознавания:', event.error);

        // Обработка no-speech отдельно - это нормальная ситуация
        if (event.error === 'no-speech') {
            this.noSpeechCount++;
            console.log(`No speech detected (попытка ${this.noSpeechCount}/${this.maxNoSpeechRetries})`);

            // Если не превышен лимит попыток - автоматически перезапускаем
            if (this.noSpeechCount < this.maxNoSpeechRetries && this.isRecording) {
                this.updateStatus('🎤 Слушаю... (говорите громче)', 'listening');
                // Перезапуск произойдет автоматически через onRecognitionEnd
                return;
            } else if (this.noSpeechCount >= this.maxNoSpeechRetries) {
                this.showError('Речь не обнаружена. Попробуйте говорить громче или проверьте микрофон.');
                this.resetRecording();
                return;
            }
        }

        // Критические ошибки
        let errorMessage = 'Ошибка распознавания речи';

        switch (event.error) {
            case 'audio-capture':
                errorMessage = 'Микрофон недоступен. Проверьте подключение.';
                break;
            case 'not-allowed':
                errorMessage = 'Доступ к микрофону запрещен. Разрешите доступ в настройках браузера.';
                break;
            case 'network':
                errorMessage = 'Ошибка сети. Проверьте подключение к интернету.';
                break;
            case 'aborted':
                // Пользователь остановил запись - не показываем ошибку
                console.log('Распознавание остановлено пользователем');
                return;
        }

        this.showError(errorMessage);
        this.resetRecording();
    }
    
    onRecognitionEnd() {
        console.log('Распознавание речи завершено');

        // Если пользователь все еще в режиме записи и не превышен лимит no-speech
        if (this.isRecording && this.noSpeechCount > 0 && this.noSpeechCount < this.maxNoSpeechRetries) {
            console.log('Автоматический перезапуск распознавания...');
            try {
                this.recognition.start();
            } catch (error) {
                console.error('Ошибка при перезапуске:', error);
                this.resetRecording();
            }
        } else {
            this.isRecording = false;
            if (this.noSpeechCount < this.maxNoSpeechRetries) {
                this.resetRecording();
            }
        }
    }
    
    async sendQuestionToServer(question) {
        try {
            // Показываем индикатор загрузки
            this.loading.style.display = 'flex';
            this.answer.style.display = 'none';
            if (this.audioControls) {
                this.audioControls.style.display = 'none';
            }
            this.updateStatus('💭 Философ размышляет...', 'thinking');

            // Отправляем запрос на сервер
            const response = await fetch('/api/ask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Скрываем индикатор загрузки
            this.loading.style.display = 'none';

            // Сохраняем ответ (но пока не показываем текст)
            this.answer.textContent = data.answer;

            // Обрабатываем аудио, если оно есть
            if (data.audio) {
                this.updateStatus('🔊 AI-Философ говорит...', 'playing');
                await this.playAudio(data.audio);
                // После воспроизведения показываем текст
                this.answer.style.display = 'block';
                this.updateStatus('✅ Ответ получен', 'success');
            } else {
                // Если нет аудио - сразу показываем текст
                this.answer.style.display = 'block';
                this.updateStatus('✅ Ответ получен (без аудио)', 'success');
            }

            // Добавляем в историю
            this.addToHistory(question, data.answer, data.audio);

        } catch (error) {
            console.error('Ошибка при отправке вопроса:', error);
            this.loading.style.display = 'none';
            this.answer.style.display = 'block';
            this.showError('Не удалось получить ответ от философа. Проверьте настройки API.');
        }
    }

    async playAudio(audioBase64) {
        try {
            // Останавливаем текущее воспроизведение, если есть
            if (this.currentAudio) {
                this.currentAudio.pause();
                this.currentAudio = null;
            }

            // Показываем анимацию говорения, скрываем текст
            this.speakingAnimation.style.display = 'flex';
            this.answer.style.display = 'none';
            if (this.audioControls) {
                this.audioControls.style.display = 'none';
            }

            // Декодируем base64 в blob
            const audioBlob = this.base64ToBlob(audioBase64, 'audio/mp3');
            this.currentAudioBlob = audioBlob;

            // Создаем URL для blob
            const audioUrl = URL.createObjectURL(audioBlob);

            // Создаем аудио элемент
            this.currentAudio = new Audio(audioUrl);

            // Обработчик окончания воспроизведения
            this.currentAudio.addEventListener('ended', () => {
                // Скрываем анимацию, показываем текст и контролы
                this.speakingAnimation.style.display = 'none';
                this.answer.style.display = 'block';
                if (this.audioControls) {
                    this.audioControls.style.display = 'flex';
                }
                this.updateStatus('✅ Воспроизведение завершено', 'success');
            });

            // Обработчик ошибки
            this.currentAudio.addEventListener('error', (e) => {
                console.error('Ошибка воспроизведения аудио:', e);
                // При ошибке тоже скрываем анимацию и показываем текст
                this.speakingAnimation.style.display = 'none';
                this.answer.style.display = 'block';
                this.updateStatus('⚠️ Ошибка воспроизведения аудио', 'error');
            });

            // Воспроизводим аудио
            await this.currentAudio.play();

        } catch (error) {
            console.error('Ошибка при воспроизведении аудио:', error);
            // При ошибке скрываем анимацию и показываем текст
            this.speakingAnimation.style.display = 'none';
            this.answer.style.display = 'block';
            this.updateStatus('⚠️ Не удалось воспроизвести аудио', 'error');
        }
    }

    base64ToBlob(base64, mimeType) {
        // Декодируем base64 в бинарные данные
        const byteCharacters = atob(base64);
        const byteArrays = [];

        for (let offset = 0; offset < byteCharacters.length; offset += 512) {
            const slice = byteCharacters.slice(offset, offset + 512);
            const byteNumbers = new Array(slice.length);

            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }

            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
        }

        return new Blob(byteArrays, { type: mimeType });
    }

    replayAudio() {
        if (this.currentAudioBlob) {
            // Показываем анимацию, скрываем текст
            this.speakingAnimation.style.display = 'flex';
            this.answer.style.display = 'none';
            if (this.audioControls) {
                this.audioControls.style.display = 'none';
            }

            const audioUrl = URL.createObjectURL(this.currentAudioBlob);
            this.currentAudio = new Audio(audioUrl);

            // Обработчик окончания воспроизведения
            this.currentAudio.addEventListener('ended', () => {
                this.speakingAnimation.style.display = 'none';
                this.answer.style.display = 'block';
                if (this.audioControls) {
                    this.audioControls.style.display = 'flex';
                }
                this.updateStatus('✅ Воспроизведение завершено', 'success');
            });

            this.currentAudio.play();
            this.updateStatus('🔊 AI-Философ говорит...', 'playing');
        }
    }
    
    addToHistory(question, answer, audioBase64 = null) {
        const timestamp = new Date().toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit'
        });

        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';

        // Добавляем кнопку воспроизведения, если есть аудио
        const audioButton = audioBase64
            ? `<button class="replay-btn" title="Воспроизвести ответ">🔊 Прослушать</button>`
            : '';

        historyItem.innerHTML = `
            <div class="question">❓ ${question}</div>
            <div class="answer">💭 ${answer}</div>
            <div class="history-footer">
                <div class="timestamp">⏰ ${timestamp}</div>
                ${audioButton}
            </div>
        `;

        // Если есть аудио, добавляем обработчик клика
        if (audioBase64) {
            const replayBtn = historyItem.querySelector('.replay-btn');
            replayBtn.addEventListener('click', () => {
                this.playAudio(audioBase64);
            });
        }

        // Добавляем в начало истории
        this.history.insertBefore(historyItem, this.history.firstChild);
    }
    
    resetRecording() {
        this.recordBtn.classList.remove('recording');
        this.recordBtn.querySelector('.btn-text').textContent = 'Нажмите, чтобы говорить';
        this.updateStatus('🎤 Готов к новому вопросу', 'ready');
    }
    
    updateStatus(text, state) {
        const statusElement = this.status;
        const statusText = statusElement.querySelector('.status-text');
        
        statusText.textContent = text;
        
        // Удаляем все классы состояний
        statusElement.classList.remove('listening', 'thinking', 'error', 'success', 'ready');
        
        // Добавляем новый класс
        if (state) {
            statusElement.classList.add(state);
        }
    }
    
    showError(message) {
        this.updateStatus(`❌ ${message}`, 'error');
        this.answer.textContent = message;
        this.answer.style.display = 'block';
        this.loading.style.display = 'none';
    }
}

// Инициализация приложения при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    new PhilosopherApp();
});
