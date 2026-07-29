# Blueprint Workflow

## Inspect

1. Find and load the Blueprint through `AssetTools`; confirm its class and path.
2. Use `BlueprintTools.list_graphs`, `list_functions`, `list_events`, and `list_variables` for structure.
3. Prefer `read_graph_dsl` to understand a whole graph. Use `find_nodes`, `get_connected_subgraph`, and `get_node_infos` for a focused event chain.
4. Read the current parent, CDO, components, and exposed properties when the requested behavior depends on them.

## Edit

1. Use function graphs for reusable or value-returning logic; keep the Event Graph for event-driven and asynchronous flow.
2. Call `get_graph_dsl_docs` before the first DSL write in a session.
3. Resolve node types with `find_node_types`; resolve exact pin names with `get_node_type_pins`.
4. Use `write_graph_dsl` for coherent graph creation or replacement; it compiles the Blueprint as part of the write. Use focused node/pin operations for small edits.
5. Add variables, parameters, dispatchers, components, or bound events before wiring logic that depends on them.
6. After non-DSL structural edits, call `compile_blueprint` once after the complete logical batch rather than after every node.

## Low-Round-Trip Path

1. Create a neutral `SceneComponent` root first with `ActorTools.add_component` when several movable or trigger components must remain independent. Add primitives or meshes beneath it; the first primitive may otherwise become the root.
2. Bootstrap all required components, variables, and bound events in one structural batch, compile once, and preserve every returned reference.
3. List all required graph operations before discovery. Resolve each exact node type once and each pin schema once; cache the results.
4. On localized editors, try compact canonical names such as `GetPlayerPawn`, `MoveComponentTo`, and `IsOverlappingActor` when spaced English display titles do not match. Use `context_pins` to disambiguate duplicate type IDs.
5. If `read_graph_dsl` omits an unconnected component-bound event, inspect the node returned by `add_component_bound_event` with `get_node_infos`; do not create duplicate events.
6. Write a coherent graph with DSL or batch the known node/pin calls through `ProgrammaticToolset`. Use individual `create_node` and `connect_pins` calls only for a genuinely small patch.
7. Make the basic behavior compile and run before adding tunable parameters, animation polish, re-entry guards, or generalized abstractions not required by the request.

## Validate

1. After `write_graph_dsl`, inspect the result of its built-in compile. Call `compile_blueprint` after non-DSL structural edits, or when later changes require compile status to be refreshed; do not compile a second time unconditionally. Under Fast validation, query focused Blueprint/compiler logs only when the compile result is ambiguous or reports a problem; Full validation includes the relevant log review.
2. Re-read the modified graph or node subgraph and verify connections and literal values.
3. Re-read variables, functions, parent, or component structure when changed.
4. Save through `AssetTools.save_assets`; confirm the asset is not dirty.
5. Use PIE only when runtime behavior must be verified.

## Hard Rules

- Pure-node outputs are recomputed for each connection; cache an expensive or stateful result in a variable when reused.
- Casting to a Blueprint creates a hard load dependency; prefer interfaces for loose coupling.
- Structural changes do not affect the generated class/CDO until compilation succeeds.
- Runtime physics requires movable components. Inspect and set mobility before enabling simulation or applying impulses.
- Preserve existing graph logic unless replacement is explicitly requested. Inspect the affected event chain before editing.
- Do not issue broad parallel `find_node_types` searches. Unreal commonly serializes them on the game thread, so a fan-out increases latency without reducing wall time.
