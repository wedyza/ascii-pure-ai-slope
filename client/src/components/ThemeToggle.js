export class ThemeToggle {
  constructor() {
    this.currentTheme = localStorage.getItem('theme') || 'dark';
    this.element = document.createElement('button');
    this.element.className = 'theme-toggle';
    this.applyTheme(this.currentTheme);
    this.render();
    this.setupEventListeners();
  }

  render() {
    this.element.textContent = this.currentTheme === 'dark' ? 'Light Mode' : 'Dark Mode';
  }

  setupEventListeners() {
    this.element.addEventListener('click', () => {
      this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
      localStorage.setItem('theme', this.currentTheme);
      this.applyTheme(this.currentTheme);
      this.render();
    });
  }

  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
  }
}
