/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        'fira-mono': ['Fira Mono'],
        'dyna-puff':['DynaPuff'],
        'roboto':['Roboto']
      }
    },
  },
  plugins: [],
}