# Introduction

gmdbuilder is a Python framework for reading, editing, and exporting Geometry Dash levels.

It is built on top of [gmdkit](https://github.com/UHDanke/gmdkit), a low-level GD serialization library by HDanke, and extends it with a type-safe, developer-friendly API.

## What it's for

gmdbuilder is the right tool for:

- **Mass automated level editing/parsing** — read and edit levels via GDShare (.gmd file) or WSLiveEditor
- **A large-scale technical level project** — an uber-solid foundation to give your project confidence as complexity increases

Every assignment is validated immediately. If you pass the wrong type, a value out of range, or a key that doesn't belong on that object, you get an error at that line.

In cases where this might be limiting/undesirable, you may opt out of this guard rail through the `setting` object.