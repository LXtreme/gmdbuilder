---
layout: home

hero:
  name: gmdbuilder
  text: Geometry Dash level scripting in Python.
  tagline: Built to help scale serious, complex GD projects.
  actions:
    - theme: brand
      text: Get Started
      link: /getting-started

features:
  - icon: 🔒
    title: Type-safe by default
    details: Every object property is validated at assignment time. Wrong types, out-of-range values, and invalid keys raise immediately — not at export.

  - icon: ⚡
    title: Full IDE support
    details: Objects are typed dicts with per-trigger TypedDict subclasses. Pylance and basedpyright give you autocomplete and inline type errors across your whole script.

  - icon: 🎮
    title: Live Editor support
    details: Connect directly to the GD WSLiveEditor to push changes into a running level in real time, without touching any files.

  - icon: 🆔
    title: Smart ID allocation
    details: level.new.group(), .item(), .color(), and .collision() scan the loaded level and hand you the next free ID — no collisions, no manual tracking.

---