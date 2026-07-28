---
name: ue5-mcp
description: Operate Unreal Engine 5 through its Model Context Protocol server with low-context tool discovery, guarded editor mutations, and post-change validation. Use for UE5 or Unreal Editor tasks involving MCP, Blueprint, actors, levels, assets, materials, PCG, Niagara, UMG, Sequencer, animation, gameplay systems, plugins, logs, screenshots, PIE, automation tests, or Live Coding; also trigger for Chinese requests mentioning UE5 MCP, Unreal MCP, 蓝图, 关卡, 材质, PCG, Niagara, UMG, 编辑器自动化, or 通过 Codex 操作虚幻引擎.
---

# UE5 MCP

Drive the live Unreal Editor through the configured `unreal-mcp` server. Keep context small by searching the bundled catalog and describing only the selected runtime toolset.

## Establish Context

1. Locate the `.uproject` from the user's path, current repository, or a focused filesystem search.
2. Read the `.uproject` and relevant config files to identify the engine association and enabled plugins. Do not scan the whole engine unless required.
3. Confirm that Unreal Editor is open with the intended project and that `unreal-mcp` responds.
4. Call `list_toolsets` only when available toolsets are unknown or the bundled catalog may be stale.
5. Read [references/router.md](references/router.md) to select a domain. Load only the reference for the current domain.

## Select Tools Economically

Use this authority order:

1. Live `describe_toolset` output from the connected editor.
2. Live tool results and object/property inspection.
3. Bundled catalog searched through `scripts/search_tools.py`.
4. Domain references in this Skill.
5. Model knowledge.

Never load all catalog JSON into context. Resolve script paths relative to this Skill directory and search the catalog instead:

```powershell
python scripts/search_tools.py "compile blueprint" --limit 8
python scripts/search_tools.py "user variables" --toolset UNiagaraToolset_System
python scripts/search_tools.py --kind skill "material"
```

If `python` is unavailable on Windows, use the Python interpreter bundled with the active UE installation under `Engine/Binaries/ThirdParty/Python3`.

Use the runtime chain `list_toolsets` (when needed) -> `describe_toolset` -> `call_tool`. After selecting a Toolset, use the exact live function name and parameter schema in `call_tool`. Do not guess signatures, enum values, node type IDs, pin names, property names, object references, or content paths.

## Execute Changes

1. Inspect the target asset, actor, graph, object, or editor state before mutation.
2. Search for reusable assets before creating replacements.
3. Check editability, checkout state, dependencies, and referencers when the operation can affect existing content.
4. Make the smallest coherent batch of changes. Keep returned object references; do not reconstruct them from display text.
5. Compile once after a logical graph-edit batch rather than after every node.
6. Save every modified asset explicitly. Confirm that it is no longer dirty when the toolset supports that check.
7. Re-read the changed structure or properties and compare them with the request.

Do not delete assets, remove actors, replace widgets, reparent Blueprints, overwrite files, or perform broad renames unless the requested scope clearly authorizes it. Inspect referencers before destructive asset operations.

## Validate Results

Choose validation proportional to the change:

- Blueprint: compile, inspect compiler messages/logs, read the changed graph, save.
- Material: recompile, inspect expressions/connections, capture an asset or viewport image when appearance matters, save.
- PCG: read graph structure, execute or regenerate the intended instance, inspect output/data view, save.
- Niagara: check compile state and stack issues, inspect summary/topology, capture the result when visual quality matters, save.
- UMG: compile the Widget Blueprint, inspect the widget tree and slot properties, capture the asset/editor view when layout matters, save.
- C++: use Live Coding only when enabled and appropriate; otherwise run the project build. Read compiler diagnostics.
- Runtime behavior: start PIE, observe logs/state, then stop PIE. Do not leave PIE running unintentionally.
- Broad or risky changes: run focused automation tests after discovery.

Read [references/diagnostics.md](references/diagnostics.md) for validation sequences. If a call fails or returns an unexpected shape, read [references/failure-patterns.md](references/failure-patterns.md) before retrying.

## Domain References

- Blueprint graph and class work: [references/blueprint.md](references/blueprint.md)
- Actors, levels, assets, objects, and editor state: [references/content-world.md](references/content-world.md)
- Materials and instances: [references/material.md](references/material.md)
- PCG graphs and instances: [references/pcg.md](references/pcg.md)
- Niagara systems and components: [references/niagara.md](references/niagara.md)
- UMG widgets: [references/umg.md](references/umg.md)
- Logging, PIE, screenshots, tests, and Live Coding: [references/diagnostics.md](references/diagnostics.md)

## Finish

Report the assets or files changed, the validations performed, and any remaining warnings. Distinguish verified results from assumptions. Do not claim success from a successful tool call alone.
