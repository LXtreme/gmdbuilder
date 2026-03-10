---
layout: home

hero:
  name: gmdbuilder
  text: Geometry Dash level scripting in Python.  
  tagline: A framework made to help scale serious, complex GD projects.
  actions:
    - theme: brand
      text: Get Started
      link: /getting-started
    
    - theme: alt
      text: Source Code
      link: 'https://github.com/LXtreme/gmdbuilder'

features:
  - icon: ✔️
    title: Type-safe by default
    details: Every object property is validated at assignment time. Wrong types, out-of-range values, and invalid keys raise immediately.

  - icon: ⚡
    title: Full IDE support
    details: Objects are fully typed such that an LSP give you autocomplete and inline type errors across your whole project.

  - icon: 
      src: /live_editor.png
      width: 64
      height: 64
    title: Live Editor support
    details: Connect directly to WSLiveEditor to hot-reload your script.

  - icon:
      src: /gdshare.png
      width: 64
      height: 64
    title: GDShare support
    details: Import and export `.gmd` files for full level editing

---