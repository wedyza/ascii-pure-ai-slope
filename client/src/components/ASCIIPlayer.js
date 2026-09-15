import { getConversionFrames, getAudioUrl } from '../services/api.js';

export class ASCIIPlayer {
  constructor() {
    this.element = document.createElement('div');
    this.element.className = 'ascii-player';
    this.frames = [];
    this.frameRate = 12;
    this.currentFrame = 0;
    this.isPlaying = false;
    this.animationId = null;
    this.audio = null;
    this.hasAudio = false;
    this.duration = 0;
    this.pendingSeek = null;
    this.render();
  }

  render() {
    this.element.innerHTML = `
      <div class="player-container">
        <pre class="ascii-display" id="ascii-display"></pre>
        <div class="player-controls">
          <button id="play-btn">Play</button>
          <input type="range" id="seek-bar" min="0" max="1000" value="0" step="1">
          <input type="range" id="volume-bar" min="0" max="100" value="100">
          <span id="time-display">0:00 / 0:00</span>
        </div>
      </div>
    `;
    this.setupControls();
  }

  setupControls() {
    const playBtn = this.element.querySelector('#play-btn');
    const seekBar = this.element.querySelector('#seek-bar');
    const volumeBar = this.element.querySelector('#volume-bar');

    playBtn.addEventListener('click', () => this.togglePlay());
    volumeBar.addEventListener('input', (e) => this.setVolume(parseInt(e.target.value)));

    seekBar.addEventListener('input', (e) => {
      const fraction = parseFloat(e.target.value) / 1000;
      const targetTime = fraction * this.duration;
      const targetFrame = Math.floor(targetTime * this.frameRate);

      this.pendingSeek = targetTime;
      this.displayFrame(targetFrame);
      this._updateSeekBar(targetTime);
      this.updateTimeDisplay();
    });
  }

  async load(conversionId) {
    const data = await getConversionFrames(conversionId);
    this.frames = data.frames;
    this.frameRate = data.frame_rate;
    this.duration = data.duration;
    this.currentFrame = 0;

    try {
      this.audio = new Audio(getAudioUrl(conversionId));
      this.audio.volume = 1.0;
      this.audio.preload = 'auto';
      this.hasAudio = true;
    } catch {
      this.audio = null;
      this.hasAudio = false;
    }

    this.displayFrame(0);
    this.updateTimeDisplay();
  }

  displayFrame(index) {
    if (index < 0 || index >= this.frames.length) return;
    this.currentFrame = index;
    this.element.querySelector('#ascii-display').textContent = this.frames[index];
  }

  togglePlay() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  play() {
    if (this.frames.length === 0) return;
    this.isPlaying = true;
    this.element.querySelector('#play-btn').textContent = 'Pause';

    if (this.audio && this.hasAudio) {
      if (this.pendingSeek !== null) {
        this.audio.currentTime = this.pendingSeek;
        this.pendingSeek = null;
      }
      this.audio.play().catch(() => {});
    }

    this.animationLoop();
  }

  pause() {
    this.isPlaying = false;
    this.element.querySelector('#play-btn').textContent = 'Play';
    if (this.audio) this.audio.pause();
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  setVolume(percent) {
    if (this.audio) {
      this.audio.volume = percent / 100;
    }
  }

  _updateSeekBar(time) {
    const seekBar = this.element.querySelector('#seek-bar');
    const fraction = this.duration > 0 ? time / this.duration : 0;
    seekBar.value = Math.round(fraction * 1000);
  }

  animationLoop() {
    if (!this.isPlaying) return;

    if (this.hasAudio && this.audio) {
      const audioTime = this.audio.currentTime;
      const expectedFrame = Math.floor(audioTime * this.frameRate);

      if (expectedFrame >= 0 && expectedFrame < this.frames.length && expectedFrame !== this.currentFrame) {
        this.displayFrame(expectedFrame);
      }

      this._updateSeekBar(audioTime);

      if (audioTime >= this.duration || this.audio.ended) {
        this.pause();
        this.displayFrame(0);
        this.audio.currentTime = 0;
        this._updateSeekBar(0);
        this.updateTimeDisplay();
        return;
      }
    } else {
      const now = performance.now();
      if (!this._lastFrameTime) this._lastFrameTime = now;
      const elapsed = now - this._lastFrameTime;
      const frameDuration = 1000 / this.frameRate;

      if (elapsed >= frameDuration) {
        const nextFrame = this.currentFrame + 1;
        if (nextFrame >= this.frames.length) {
          this.pause();
          this.displayFrame(0);
          this.updateTimeDisplay();
          return;
        }
        this.displayFrame(nextFrame);
        this._lastFrameTime = now - (elapsed % frameDuration);
      }
    }

    this.updateTimeDisplay();
    this.animationId = requestAnimationFrame(() => this.animationLoop());
  }

  updateTimeDisplay() {
    const timeDisplay = this.element.querySelector('#time-display');
    let currentTime;
    if (this.hasAudio && this.audio) {
      currentTime = this.audio.currentTime;
    } else {
      currentTime = this.currentFrame / this.frameRate;
    }
    timeDisplay.textContent = `${this.formatTime(currentTime)} / ${this.formatTime(this.duration)}`;
  }

  formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }
}
