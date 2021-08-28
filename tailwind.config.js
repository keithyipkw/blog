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
      safelist: ['font-content-serif', ...axiomTailwindConfig.purge.options.safelist]
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
    },
  },
}
