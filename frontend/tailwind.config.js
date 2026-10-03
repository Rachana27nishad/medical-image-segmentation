/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        medical: {
          dark: '#0B132B',
          navy: '#1C2541',
          slate: '#3A506B',
          cyan: '#00B4D8',
          teal: '#00F5D4',
          accent: '#7209B7',
          success: '#10B981',
          warning: '#F59E0B',
          danger: '#EF4444'
        }
      }
    },
  },
  plugins: [],
}
