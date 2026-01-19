# gmdbuilder – TODO

URGENT ! ! ! !



## Core Foundations (Must-Have)
- Safe wrapper around `gmdkit.Level`
- Central object queue with validate-on-add
- Full validation pass before export
- Ability to disable specific validations when needed

## Property Validation
- Type checking for properties
- Required property enforcement
- Value range checks (time, easing, distances, etc.)
- Valid group reference checking
- Extensible / custom validator support

## Group Management
- Group allocation (single IDs and ranges)
- Collision and overlap detection
- Solid vs callable group distinction
- Placeholder / unresolved group support
- Group usage queries (“what uses this group?”)
- Export-time group resolution

## Export Pipeline
- Resolve placeholder groups
- Deterministic export to gmdkit Level
- Optional JSON export for tooling/debugging
- Export summary (object count, group count, warnings)

## Trigger Ordering & GD Constraints
- Spawn trigger tracking
- Spawn limit warnings/errors
- Trigger dependency detection
- Automatic trigger ordering
- Circular dependency detection
- Manual ordering override if needed

## Remap System
- Remap string builder (property 442)
- Remap validation
- Multi-target remaps
- Common helpers (toggles, off-switches)
- Parse existing remap strings

## Property & Context Utilities
- Property defaults system
- Property normalization helpers
- Common property bundles (fade, rotate, etc.)
- Context stack (`with`-based temporary state)
- Automatic cleanup on context exit

## Budget & Inspection Tools
- Track object count
- Track group usage
- Track trigger counts by type
- Warnings near GD limits
- Queue, group, and dependency inspection helpers

## Type Safety
- Full type hints for public APIs
- TypedDicts for common trigger structures
- Literal types where useful (property IDs)
- Static type checking (basedpyright)

## CLI Tools (Nice-to-Have)
- GD object string → Python dict converter
- Optional level validation CLI
- Group usage inspection CLI

## Documentation & Examples (Later)
- Getting started guide
- Core concepts (safety, groups, validation)
- Simple trigger example
- Touhou component system example
- API reference

## Testing & Distribution (Later)
- Unit tests for validators and export pipeline
- PyPI packaging
- Versioning and changelog
- Release automation
