
        const timerDisplay = document.querySelector('.timer-text');
        const timerImage = document.querySelector('.timer-image');
        const startBtn = document.querySelector('.start-btn');
        const resetBtn = document.querySelector('.reset-btn');
        const timeInput = document.querySelector('.time-input');
        const methodBtns = document.querySelectorAll('.method-btn');
        const suggestedTimeSpan = document.querySelector('.suggested-time span');

        let timeLeft = 0;
        let timerId = null;
        let rotation = 0;
        let currentMethod = 'boil';

        // Convert MM:SS to seconds
        function timeToSeconds(timeStr) {
            const [minutes, seconds] = timeStr.split(':').map(Number);
            return minutes * 60 + seconds;
        }

        // Convert seconds to MM:SS
        function secondsToTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
        }

        // Update timer display
        function updateDisplay() {
            timerDisplay.textContent = secondsToTime(timeLeft);
            rotation = (rotation + 6) % 360;
            timerImage.style.transform = `rotate(${rotation}deg)`;
        }

        // Start/Pause timer
        startBtn.addEventListener('click', () => {
            if (timerId) {
                // Pause
                clearInterval(timerId);
                timerId = null;
                startBtn.textContent = '▶';
            } else {
                // Start
                if (!timeLeft && timeInput.value) {
                    timeLeft = timeToSeconds(timeInput.value);
                }
                if (timeLeft > 0) {
                    timerId = setInterval(() => {
                        timeLeft--;
                        updateDisplay();
                        if (timeLeft === 0) {
                            clearInterval(timerId);
                            timerId = null;
                            startBtn.textContent = '▶';
                            alert('Cooking time is up!');
                        }
                    }, 1000);
                    startBtn.textContent = '⏸';
                }
            }
        });

        // Reset timer
        resetBtn.addEventListener('click', () => {
            clearInterval(timerId);
            timerId = null;
            timeLeft = 0;
            rotation = 0;
            timeInput.value = '';
            timerDisplay.textContent = '00:00';
            timerImage.style.transform = 'rotate(0deg)';
            startBtn.textContent = '▶';
        });

        // Method selection
        methodBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                methodBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentMethod = btn.dataset.method;
                timeInput.value = btn.dataset.time;
                suggestedTimeSpan.textContent = btn.dataset.time;
                
                // Reset timer when changing method
                clearInterval(timerId);
                timerId = null;
                timeLeft = 0;
                rotation = 0;
                timerDisplay.textContent = '00:00';
                timerImage.style.transform = 'rotate(0deg)';
                startBtn.textContent = '▶';
            });
        });

        // Input validation
        timeInput.addEventListener('input', (e) => {
            const value = e.target.value;
            if (value.length === 2 && !value.includes(':')) {
                e.target.value = value + ':';
            }
            if (value.length > 5) {
                e.target.value = value.slice(0, 5);
            }
        });