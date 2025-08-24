document.addEventListener('DOMContentLoaded', () => {
    const audioPlayer = document.getElementById('audioPlayer');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');
    const currentTimeSpan = document.getElementById('currentTime');
    const durationSpan = document.getElementById('duration');
    const volumeSlider = document.getElementById('volumeSlider');
    const muteBtn = document.getElementById('muteBtn');

    let isPlaying = false;
    let isMuted = false;
    let previousVolume = 1;

    // --- Play/Pause Functionality ---
    playPauseBtn.addEventListener('click', () => {
        if (isPlaying) {
            audioPlayer.pause();
            playPauseBtn.classList.remove('playing');
        } else {
            audioPlayer.play();
            playPauseBtn.classList.add('playing');
        }
        isPlaying = !isPlaying;
    });

    // --- Time Update & Progress Bar ---
    audioPlayer.addEventListener('timeupdate', () => {
        const currentTime = audioPlayer.currentTime;
        const duration = audioPlayer.duration;

        if (!isNaN(duration)) {
            const progressPercent = (currentTime / duration) * 100;
            progressFill.style.width = `${progressPercent}%`;
            currentTimeSpan.textContent = formatTime(currentTime);
        }
    });

    // --- Set Duration when metadata is loaded ---
    audioPlayer.addEventListener('loadedmetadata', () => {
        durationSpan.textContent = formatTime(audioPlayer.duration);
        volumeSlider.value = audioPlayer.volume; // Initialize slider with current volume
    });

    // --- Handle seeking when progress bar is clicked ---
    progressBar.addEventListener('click', (e) => {
        const progressBarWidth = progressBar.clientWidth;
        const clickX = e.offsetX; // Get click position relative to the element
        const seekTime = (clickX / progressBarWidth) * audioPlayer.duration;
        audioPlayer.currentTime = seekTime;
    });

    // --- Volume Control ---
    volumeSlider.addEventListener('input', () => {
        audioPlayer.volume = volumeSlider.value;
        // Update mute button icon based on volume
        if (audioPlayer.volume === 0) {
            muteBtn.classList.add('muted');
            isMuted = true;
        } else {
            muteBtn.classList.remove('muted');
            isMuted = false;
        }
    });

    muteBtn.addEventListener('click', () => {
        if (isMuted) {
            audioPlayer.volume = previousVolume; // Restore previous volume
            volumeSlider.value = previousVolume;
            muteBtn.classList.remove('muted');
        } else {
            previousVolume = audioPlayer.volume; // Save current volume
            audioPlayer.volume = 0;
            volumeSlider.value = 0;
            muteBtn.classList.add('muted');
        }
        isMuted = !isMuted;
    });

    // --- Utility function to format time ---
    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        const formattedSeconds = remainingSeconds < 10 ? `0${remainingSeconds}` : remainingSeconds;
        return `${minutes}:${formattedSeconds}`;
    }

    // --- Handle track ending ---
    audioPlayer.addEventListener('ended', () => {
        isPlaying = false;
        playPauseBtn.classList.remove('playing');
        audioPlayer.currentTime = 0; // Reset to beginning
        progressFill.style.width = '0%';
        currentTimeSpan.textContent = formatTime(0);
    });

    // Initial state for play/pause button (optional, but good practice)
    if (audioPlayer.paused) {
        playPauseBtn.classList.remove('playing');
    } else {
        playPauseBtn.classList.add('playing');
    }

    // Initial state for mute button
    if (audioPlayer.volume === 0 || audioPlayer.muted) {
        muteBtn.classList.add('muted');
        isMuted = true;
    } else {
        muteBtn.classList.remove('muted');
        isMuted = false;
    }
});