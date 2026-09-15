import { uploadVideo, getConversionStatus } from '../services/api.js';

export class UploadForm {
  constructor(onConversionReady) {
    this.onConversionReady = onConversionReady;
    this.element = document.createElement('div');
    this.element.className = 'upload-form';
    this.render();
    this.setupEventListeners();
  }

  render() {
    this.element.innerHTML = `
      <div class="upload-area" id="drop-zone">
        <input type="file" id="file-input" accept="video/mp4,video/webm,video/avi,video/quicktime" hidden>
        <p>Drop a video file here or <button id="browse-btn">Browse</button></p>
        <p class="upload-hint">Max 5 minutes, up to 100MB</p>
      </div>
      <div class="upload-progress hidden" id="upload-progress">
        <div class="progress-bar">
          <div class="progress-fill" id="progress-fill"></div>
        </div>
        <p id="progress-text">Uploading...</p>
      </div>
      <div class="upload-error hidden" id="upload-error">
        <p id="error-text"></p>
      </div>
    `;
  }

  setupEventListeners() {
    const dropZone = this.element.querySelector('#drop-zone');
    const fileInput = this.element.querySelector('#file-input');
    const browseBtn = this.element.querySelector('#browse-btn');

    browseBtn.addEventListener('click', (e) => {
      e.preventDefault();
      fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        this.handleFile(e.target.files[0]);
      }
    });

    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
      dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropZone.classList.remove('dragover');
      if (e.dataTransfer.files.length > 0) {
        this.handleFile(e.dataTransfer.files[0]);
      }
    });
  }

  async handleFile(file) {
    const dropZone = this.element.querySelector('#drop-zone');
    const progress = this.element.querySelector('#upload-progress');
    const errorDiv = this.element.querySelector('#upload-error');
    const progressFill = this.element.querySelector('#progress-fill');
    const progressText = this.element.querySelector('#progress-text');

    dropZone.classList.add('hidden');
    errorDiv.classList.add('hidden');
    progress.classList.remove('hidden');

    try {
      progressText.textContent = 'Uploading...';
      progressFill.style.width = '50%';

      const result = await uploadVideo(file);

      progressText.textContent = 'Converting...';
      progressFill.style.width = '75%';

      await this.pollConversion(result.id);
    } catch (err) {
      progress.classList.add('hidden');
      dropZone.classList.remove('hidden');
      errorDiv.classList.remove('hidden');
      this.element.querySelector('#error-text').textContent = err.message;
    }
  }

  async pollConversion(id) {
    const progressFill = this.element.querySelector('#progress-fill');
    const progressText = this.element.querySelector('#progress-text');

    while (true) {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const status = await getConversionStatus(id);

      if (status.status === 'ready') {
        progressFill.style.width = '100%';
        progressText.textContent = 'Done!';
        this.onConversionReady(id);
        return;
      } else if (status.status === 'error') {
        throw new Error(status.message);
      }

      progressText.textContent = status.message;
      progressFill.style.width = `${status.progress * 100}%`;
    }
  }
}
