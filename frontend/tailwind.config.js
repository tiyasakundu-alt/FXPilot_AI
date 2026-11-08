/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        fx: {
          bg: 'var(--fx-bg-main)',
          sidebar: 'var(--fx-bg-sidebar)',
          card: 'var(--fx-bg-card)',
          elevated: 'var(--fx-bg-elevated)',
          teal: 'var(--fx-primary-teal)',
          'teal-soft': 'var(--fx-soft-teal)',
          green: 'var(--fx-positive-green)',
          red: 'var(--fx-negative-red)',
          text: 'var(--fx-main-text)',
          muted: 'var(--fx-secondary-text)',
          border: 'var(--fx-border)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      boxShadow: {
        'subtle': '0 1px 3px 0 rgba(0, 0, 0, 0.15), 0 1px 2px -1px rgba(0, 0, 0, 0.1)',
        'elevated': '0 4px 12px -2px rgba(0, 0, 0, 0.25), 0 2px 6px -2px rgba(0, 0, 0, 0.15)',
        'glow-teal': '0 0 20px -3px rgba(25, 195, 177, 0.25)',
      },
    },
  },
  plugins: [],
};
