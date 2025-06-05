/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,jsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: '#12151C',
        text: '#DDD6C5',
        primary: '#F2B705',
        accent: '#C0402F',
        secondary: '#2C2F48',
        border: '#3C3B37',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
