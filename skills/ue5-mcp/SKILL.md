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

Work in stages so discovery is complete before each coherent mutation batch.

### Phase 1: Preflight

1. Inspect the target asset, actor, graph, object, and relevant editor state without mutating them.
2. Search for reusable assets before creating replacements.
3. Check editability, checkout state, dependencies, and referencers when the operation can affect existing content.
4. Gather independent read-only facts together when the connected editor can handle them safely.

### Phase 2: Bootstrap

Create only the minimum asset shell, component, graph, or instance needed to obtain live object references. Skip this phase for existing targets. Preserve every returned reference and do not build dependent logic yet.

### Phase 3: Discover

Using the live references, resolve all property names, schemas, node types, pin names, enum values, and dependent objects needed for the next edit batch. Finish discovery before mutation; if later discovery depends on a newly created object, start another explicit bootstrap/discover cycle.

### Phase 4: Execute

1. Apply the smallest coherent batch of changes and reuse returned references instead of reconstructing them from display text.
2. Compile or recompile once after the complete logical batch. Treat a Toolset operation with a documented built-in compile as that compile; do not compile a second time unconditionally.
3. If a mutation fails or returns an unexpected shape, stop and read [references/failure-patterns.md](references/failure-patterns.md) before retrying.

### Phase 5: Validate And Save

Select the validation level below, follow the selected domain reference and validation level, save every modified asset explicitly, and confirm that each saved asset is no longer dirty when supported.

Do not delete assets, remove actors, replace widgets, reparent Blueprints, overwrite files, or perform broad renames unless the requested scope clearly authorizes it. Inspect referencers before destructive asset operations.

## Validate Results

Default to **Fast** validation for isolated, routine, narrowly scoped mutations. Fast validation still requires a targeted readback of the exact properties, connections, or structure changed; compile and save success alone are insufficient.

Escalate to **Full** validation when the user requests runtime proof, the change affects visual or runtime behavior, the target is shared or high-risk, the change spans multiple assets, or Fast evidence is ambiguous. Read [references/diagnostics.md](references/diagnostics.md) for the exact levels and for logs, images, PIE, tests, and Live Coding. Use the selected domain reference for its required minimum evidence.

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
