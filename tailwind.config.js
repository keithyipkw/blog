const defaultTheme = require('tailwindcss/defaultTheme')
const axiomTailwindConfig = require('./themes/axiom/tailwind.config.js');

module.exports = {
  presets: [
    axiomTailwindConfig
  ],
  purge: {
    enabled: true,
    layers: axiomTailwindConfig.purge.layers,
    content: ['./*(layouts|content|data|static)/**/*.*(html|toml|md)', './themes/axiom/*(layouts|content|data|static)/**/*.*(html|toml|md)'],
    options: {
      safelist: ['font-content-serif', 'w-xs','w-sm','w-md','w-lg','w-xl','w-2xl','w-3xl','w-4xl','w-5xl','w-6xl','w-7xl', ...axiomTailwindConfig.purge.options.safelist]
    }
  },
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Noto Sans', ...defaultTheme.fontFamily.sans],
        'serif': ['Noto Serif', ...defaultTheme.fontFamily.serif],
        'mono': ['Noto Mono', ...defaultTheme.fontFamily.mono],
        'basic-sans': ['Noto Sans', ...defaultTheme.fontFamily.sans],
        'content-sans': ['Noto Sans', ...defaultTheme.fontFamily.sans],
        'content-serif': ['Noto Serif', ...defaultTheme.fontFamily.serif],
        'content-title': ['Noto Sans', ...defaultTheme.fontFamily.sans],
      },
      width: {
        'xs': '20rem',
        'sm': '24rem',
        'md': '28rem',
        'lg': '32rem',
        'xl': '36rem',
        '2xl': '42rem',
        '3xl': '48rem',
        '4xl': '56rem',
        '5xl': '64rem',
        '6xl': '72rem',
        '7xl': '80rem',
      },
    },
  },
}
