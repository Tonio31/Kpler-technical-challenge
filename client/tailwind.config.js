/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'app-yellow-100': '#F9f3e6',
        'app-yellow-500': '#f9d86c',
        'app-yellow-700': '#e6b409',
        'app-yellow-900': '#9a7a0f'
      },
      maxWidth: {
        content: '1200px'
      }
    }
  },
  plugins: []
};
