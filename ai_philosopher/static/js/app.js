// AI-Философ - Real-time голосовое взаимодействие

class PhilosopherApp {
    constructor() {
        this.recognition = null;
        this.isRecording = false;
        this.currentTranscript = '';
        
        // DOM элементы
        this.recordBtn = document.getElementById('recordBtn');
        this.status = document.getElementById('status');
        this.transcript = document.getElementById('transcript');
        this.answer = document.getElementById('answer');
        this.loading = document.getElementById('loading');
        this.history = document.getElementById('history');
        
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
        
        console.log('AI-Философ инициализирован');
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
        console.error('Ошибка распознавания:', event.error);
        
        let errorMessage = 'Ошибка распознавания речи';
        
        switch (event.error) {
            case 'no-speech':
                errorMessage = 'Речь не обнаружена. Попробуйте снова.';
                break;
            case 'audio-capture':
                errorMessage = 'Микрофон недоступен. Проверьте подключение.';
                break;
            case 'not-allowed':
                errorMessage = 'Доступ к микрофону запрещен. Разрешите доступ в настройках браузера.';
                break;
            case 'network':
                errorMessage = 'Ошибка сети. Проверьте подключение к интернету.';
                break;
        }
        
        this.showError(errorMessage);
        this.resetRecording();
    }
    
    onRecognitionEnd() {
        console.log('Распознавание речи завершено');
        this.isRecording = false;
        this.resetRecording();
    }
    
    async sendQuestionToServer(question) {
        try {
            // Показываем индикатор загрузки
            this.loading.style.display = 'flex';
            this.answer.style.display = 'none';
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
            this.answer.style.display = 'block';
            
            // Отображаем ответ
            this.answer.textContent = data.answer;
            this.updateStatus('✅ Ответ получен', 'success');
            
            // Добавляем в историю
            this.addToHistory(question, data.answer);
            
        } catch (error) {
            console.error('Ошибка при отправке вопроса:', error);
            this.loading.style.display = 'none';
            this.answer.style.display = 'block';
            this.showError('Не удалось получить ответ от философа. Проверьте настройки API.');
        }
    }
    
    addToHistory(question, answer) {
        const timestamp = new Date().toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
            <div class="question">❓ ${question}</div>
            <div class="answer">💭 ${answer}</div>
            <div class="timestamp">⏰ ${timestamp}</div>
        `;
        
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
