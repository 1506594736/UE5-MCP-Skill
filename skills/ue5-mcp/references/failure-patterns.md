# Failure Patterns

| Symptom | Likely cause | Response |
|---|---|---|
| Toolset or tool not found | Bundled snapshot differs from running editor | Call `list_toolsets`, then live `describe_toolset`; trust runtime names |
| Toolset description is huge or truncated | Too many Toolsets were described or the complete schema was emitted | Select one primary Toolset and extract only the specific tool names and schemas needed |
| Parameter/schema rejection | Guessed or stale signature | Describe the Toolset again and rebuild arguments from its schema |
| Null or invalid object | Wrong content path, unloaded object, stale returned reference | Find/load again and preserve the new returned reference |
| Property call succeeds but value is unchanged | Wrong owner or guessed property name | Inspect components; run `list_properties`, read, write, and read back |
| Blueprint nodes fail to connect | Wrong node type or pin name | Use `find_node_types` and `get_node_type_pins`; inspect current nodes |
| English Blueprint node search returns no matches | Localized title or compact function token differs from the display name | Try the compact canonical name, then `context_pins`; stop after two misses and inspect live nodes or catalog evidence |
| Many parallel editor searches remain slow | Unreal serialized the calls on the game thread | Stop the fan-out; batch known calls or perform the minimum dependent calls sequentially |
| First primitive unexpectedly becomes the Blueprint root | Primitive was added before a neutral scene root | Create a `SceneComponent` root first with `ActorTools.add_component`, then parent independent components deliberately |
| One Blueprint graph takes many node-by-node calls | A coherent edit was split into high-latency MCP round trips | Discover schemas first, then use `write_graph_dsl` or `ProgrammaticToolset` for the mutation batch |
| Structural Blueprint change is absent | Blueprint not compiled after batch | Compile, inspect errors, then re-read class/CDO/graph |
| UMG layout does not change | Slot property was guessed or wrong slot class used | Inspect the returned Slot with `ObjectTools` and write exact names |
| Niagara compiles but renders nothing | Spawn/lifetime/bounds/material/namespace/renderer dependency | Inspect summary, topology, stack issues, material, bounds, and component overrides |
| PCG graph executes with no output | Wrong pins/settings, empty spatial input, wrong instance | Read schema, structure, instance params, node data view, and logs |
| PCG data view has no inspection data | Inspection was not enabled before the last execution | Call `GetNodeDataView` once to enable inspection, execute and await one instance, then call `GetNodeDataView` again |
| Editor freezes while inspecting PCG actors | Actors sharing one graph were inspected concurrently | Stop concurrent calls; inspect each actor's shared graph serially and await every step |
| Asset remains dirty | Save omitted or failed | Save exact asset paths, read logs, verify editability and dirty state |
| Async call appears incomplete | Result was treated as synchronous | Wait/poll the returned async result or status tool before evaluating |
| MCP disconnects | Editor closed, wrong project, server unavailable | Stop mutations; confirm editor/project and MCP endpoint before retrying |
| Screenshot is blank or irrelevant | Wrong editor/viewport target or capture timing | Focus/open the target, wait for render, capture again, inspect image content |

Retry a failed mutation only after gathering new evidence. Do not repeat the same guessed call with small parameter variations.
