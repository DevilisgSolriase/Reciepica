/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./Frontend/templates/*.html'],
  theme: {
    extend: {
      colors: {
        'french-dark-blue': '#1d3557',
        'french-very-dark-blue': '#122f59',
        'frencg-light-blue': '#457b9d',
        'french-Very-light-blue': '#3d6098',
        'french-white': '#e7e7e7',
        'french-red': '#e63946'
      },
      fontFamily: {
        LeFont: ['Caveat']
      },
      height: {
        '82': '22rem'
      }

    },
  },
  plugins: [],
}

