# Material Workflow

## Choose The Asset Type

1. Search for an existing Material or Material Instance that satisfies the request.
2. Create a Material Instance when a suitable parent already exists.
3. Create a new Material only when no suitable parent exists.
4. Search for reusable Material Functions before implementing shared graph logic.

## Author

1. Inspect expression classes and existing expressions.
2. Query exact expression input/output names before connecting nodes.
3. Expose values that users should tune as parameters and group related parameters consistently.
4. Lay out expressions after topology is complete.
5. Remove unused expressions only after checking that the deletion matches the requested scope.

## Validate

1. Recompile the Material.
2. Inspect expressions, inputs, connections, and output property connections.
3. Capture the asset or viewport when appearance matters.
4. Save and verify dirty state.

## Hard Rules

- A neutral tangent-space normal is `(0, 0, 1)`, not zero.
- Static switches multiply shader permutations; keep them limited.
- Do not edit engine-content Materials or Instances directly. Duplicate into project content first.
- Confirm parameter names and types before setting a Material Instance value.
