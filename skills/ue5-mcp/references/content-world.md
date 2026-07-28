# Content And World Workflow

## Assets

1. Normalize content paths to Unreal paths such as `/Game/...`; do not confuse them with filesystem paths.
2. Use `AssetTools.find_assets`, `exists`, `get_asset_class`, and registry tags before loading broadly.
3. Check `can_edit_asset` and source-control state before modification.
4. Inspect referencers and dependencies before move, rename, replacement, or deletion.
5. Save modified assets explicitly and verify dirty state.

## Actors And Levels

1. Confirm the current level with `SceneTools.get_current_level`.
2. Find actors by stable criteria and inspect labels, classes, tags, transforms, and components.
3. Keep the returned actor/component references for later calls.
4. Modify component-owned properties on the component, not the actor. This is especially important for lights, atmosphere, fog, clouds, meshes, and post-process components.
5. Save affected actors/levels after changes.

## Properties

1. Call `ObjectTools.list_properties` on an unfamiliar object.
2. Read exact current values with `get_properties`.
3. Write only discovered property names with `set_properties`.
4. Re-read the same properties and compare values. A successful call without a matching readback is not proof of success.

## Visual Work

Capture a baseline before lighting, composition, material, UI, Niagara, or camera changes. Apply a focused change, capture again, and compare. Limit blind refinement cycles; report the remaining mismatch after three unsuccessful visual iterations.
