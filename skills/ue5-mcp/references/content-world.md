# Content And World Workflow

## Inspect

1. Normalize content paths to Unreal paths such as `/Game/...`; do not confuse them with filesystem paths.
2. Use `AssetTools.find_assets`, `exists`, `get_asset_class`, and registry tags before loading broadly.
3. Check `can_edit_asset` and source-control state before modification. Inspect referencers and dependencies before move, rename, replacement, or deletion.
4. Confirm the current level with `SceneTools.get_current_level` before actor or level work.
5. Find actors by stable criteria and inspect labels, classes, tags, transforms, outliner folders, and components.
6. Call `ObjectTools.list_properties` on unfamiliar objects, then read exact current values with `get_properties`.

## Modify

1. Keep returned actor and component references for later calls.
2. Write only property names discovered through inspection.
3. Modify component-owned properties on the component, not the actor. This is especially important for lights, atmosphere, fog, clouds, meshes, and post-process components.
4. Keep actor, folder, and level changes within the current level unless loading another level is explicitly required.

## Validate

1. Re-read every changed property and compare it with the requested value.
2. Re-read actor transforms, labels, tags, outliner folder membership, and component structure when any of them changed.
3. Call `SceneTools.get_current_level` again after level loading or level-sensitive operations and verify the expected level remains active.
4. Use viewport or editor captures when placement, composition, lighting, or other visual state matters.

## Save

1. Use `SceneTools.save_actor` for affected actors.
2. Use `AssetTools.save_assets` for modified asset paths, including the level asset when the level package changed, then verify dirty state where supported.
3. The current MCP catalog has no dedicated `save_level` tool. Do not claim that one was called; if the available save operations cannot persist a level change, report that limitation explicitly.

## Visual Work

Capture a baseline before lighting, composition, material, UI, Niagara, or camera changes. Apply a focused change, capture again, and compare. Limit blind refinement cycles; report the remaining mismatch after three unsuccessful visual iterations.
