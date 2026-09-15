import { UploadForm } from '../components/UploadForm.js';
import { ASCIIPlayer } from '../components/ASCIIPlayer.js';
import { ThemeToggle } from '../components/ThemeToggle.js';
import { setCurrentConversion, setupCleanupOnUnload } from '../services/api.js';

export class Home {
  constructor() {
    this.element = document.createElement('div');
    this.element.className = 'home';
    this.player = null;
    this.render();
    setupCleanupOnUnload();
  }

  render() {
    this.element.innerHTML = `
      <header>
        <h1>PodSite - Video to ASCII Player</h1>
        <div id="theme-container"></div>
      </header>
      <main>
        <section id="upload-section">
          <div id="upload-container"></div>
        </section>
        <section id="player-section" class="hidden">
          <div id="player-container"></div>
        </section>
      </main>
    `;

    const themeToggle = new ThemeToggle();
    this.element.querySelector('#theme-container').appendChild(themeToggle.element);

    const uploadForm = new UploadForm((conversionId) => this.onConversionReady(conversionId));
    this.element.querySelector('#upload-container').appendChild(uploadForm.element);
  }

  async onConversionReady(conversionId) {
    const playerSection = this.element.querySelector('#player-section');
    const playerContainer = this.element.querySelector('#player-container');

    playerSection.classList.remove('hidden');

    this.player = new ASCIIPlayer();
    playerContainer.appendChild(this.player.element);

    setCurrentConversion(conversionId);
    await this.player.load(conversionId);
  }
}
