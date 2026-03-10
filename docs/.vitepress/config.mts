import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "gmdbuilder",
  description: "A type-safe Python framework for Geometry Dash level editing and scripting.",

  base: '/gmdbuilder/',

  head: [
    ['link', { rel: 'icon', href: '/gmdbuilder/favicon.ico' }],
  ],

  themeConfig: {
    logo: '/logo.png',
    siteTitle: 'gmdbuilder',

    nav: [
      { text: 'Guide', link: '/getting-started' },
      { text: 'Reference', link: '/reference' },
      {
        text: 'Links',
        items: [
          { text: 'PyPI', link: 'https://pypi.org/project/gmdbuilder/' },
          { text: 'gmdkit', link: 'https://github.com/UHDanke/gmdkit' },
          { text: 'GD Editor Docs', link: 'https://github.com/UHDanke/gd_docs' },
          { text: 'Flowvix GD Info Explorer', link: 'https://flowvix.github.io/gd-info-explorer/' },
        ]
      }
    ],

    sidebar: [
      {
        text: 'Guide',
        items: [
          { text: 'Getting Started',     link: '/getting-started' },
          { text: 'Add & Edit Objects',  link: '/objects' },
          { text: 'Object Types',        link: '/object-types' },
          { text: 'New IDs',             link: '/new-ids' },
          { text: 'Colors',              link: '/colors' },
          { text: 'Validation Settings', link: '/setting' },
        ]
      },
      {
        text: 'Reference',
        items: [
          { text: 'Property Search',     link: '/reference' },
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/LXtreme/gmdbuilder' }
    ],

    search: {
      provider: 'local'
    },

    footer: {
      // message: 'Released under the MIT License.',
      copyright: 'gmdbuilder — built in collaboration with <a href="https://github.com/UHDanke">HDanke</a>'
    },

    // editLink: {
    //   pattern: 'https://github.com/LXtreme/gmdbuilder/edit/main/docs/:path',
    //   text: 'Edit this page on GitHub'
    // },
  },

  markdown: {
    theme: {
      light: 'one-light',
      dark:  'one-dark-pro',
    },
    lineNumbers: true,
  },
})