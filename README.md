![PyPI](https://img.shields.io/pypi/v/gmdkit?style=flat-square)
![Python](https://img.shields.io/pypi/pyversions/gmdkit?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

# gmdbuilder
An unopinionated General-Purpose Geometry Dash framework for safe and easy level editing and scripting.
**Build on a solid foundation, not inside a cage.**

Many tools already tackle this problem, and if you take a step back from it, it becomes clear the main concern is building dictionaries of property-value pairs.
The goal of this project is to realize that for GD project development:
- Every project's needs vary an insane amount
- Developers should know exactly what theyre placing in the level
- Developers should be focused on the level, not on syntax
- GD 2.2 has added so much that any opinionated way of doing things is far too limiting.

## Why Python?

You may not realize it at first, but Python is among the most ideal languages for the task:
- Any programming paradigm that you need has full type and syntax support
- "Python is slow" doesn't matter if the program's runtime is under 0.1 seconds
- Type system is as convenient or precise as you need
- Huge package ecosystem
- Well known and beginner friendly
