# Niagara Workflow

## Inspect

1. Search Niagara assets before creating a new System.
2. Read system summary, schema, dependencies, compile state, and stack issues.
3. Read emitter, stack, module, renderer, dynamic-input, and data-interface schemas only for the area being changed.
4. Inspect current topology and values before editing.

## Edit

1. Prefer a suitable template or existing reusable System.
2. Add emitters, modules, renderers, user variables, and set-parameter entries with live schema data.
3. Respect stack order, parameter namespaces, simulation target, coordinate space, lifecycle, bounds, and renderer/material dependencies.
4. Use component Toolsets for placed/runtime overrides and System Toolsets for asset authoring.
5. Remove modules, renderers, variables, or emitters only after confirming they are unused and within scope.

## Validate

1. Read `GetSystemCompileState` and `GetStackIssues`.
2. Apply an automatic issue fix only after inspecting what it changes.
3. Re-read summary, topology, dependencies, user variables, and changed values.
4. Capture a viewport image or run PIE for appearance/lifetime checks.
5. Save the System and any dependent Material or Blueprint assets.

## Silent Failure Checks

- Dynamic Material Parameters require matching Material nodes and channel layout.
- SubUV animation requires matching renderer grid, update module, and renderer-info input.
- Renderer Info data interfaces must point to the intended renderer.
- A valid stack edit can still render nothing because of bounds, material, visibility, lifetime, spawn rate, or parameter namespace.
