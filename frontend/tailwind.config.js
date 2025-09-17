/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'rain-dark': '#0a0a0a',
        'rain-darker': '#050505',
        'rain-pink': '#ff0080',
        'rain-pink-dark': '#e0006f',
        'rain-gray': '#1a1a1a',
        'rain-gray-light': '#2a2a2a',
        'rain-gray-lighter': '#3a3a3a',
        'rain-text': '#e5e5e5',
        'rain-text-dim': '#999999',
      },
      fontFamily: {
        'sans': ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}