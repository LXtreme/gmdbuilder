---
layout: home

hero:
  name: gmdbuilder
  text: Geometry Dash level scripting in Python.
  tagline: Type-safe objects, auto-validation, and live editor support — built for people who want to write real code, not click buttons.
  actions:
    - theme: brand
      text: Get Started
      link: /getting-started
    - theme: alt
      text: Introduction
      link: /introduction

features:
  - icon: 🔒
    title: Type-safe by default
    details: Every object property is validated at assignment time. Wrong types, out-of-range values, and invalid keys raise immediately — not at export.

  - icon: 🧠
    title: Full IDE support
    details: Objects are typed dicts with per-trigger TypedDict subclasses. Pylance and basedpyright give you autocomplete and inline type errors across your whole script.

  - icon: 🎮
    title: Live editor support
    details: Connect directly to the GD WSLiveEditor to push changes into a running level in real time, without touching any files.

  - icon: 🆔
    title: Smart ID allocation
    details: level.new.group(), .item(), .color(), and .collision() scan the loaded level and hand you the next free ID — no collisions, no manual tracking.

  - icon: 🎨
    title: Color channel control
    details: Read and write any color channel as a plain Python dataclass. Changes round-trip cleanly through file or live editor export.

  - icon: ⚡
    title: No boilerplate
    details: Load a level in one line. Objects are plain dicts you can slice, filter, and extend with normal Python. No wrappers to learn, no magic to fight.
---