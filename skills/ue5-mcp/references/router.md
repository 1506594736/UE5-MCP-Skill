# Toolset Router

Select one primary domain, search the catalog, then describe only the live Toolsets needed for the task. Add general Toolsets only when required.

| Intent | Start with | Add when needed | Domain reference |
|---|---|---|---|
| Assets and folders | `AssetTools` | `ObjectTools`, `UEditorAppToolset` | `content-world.md` |
| Actors and levels | `SceneTools` | `ActorTools`, `ObjectTools`, `PrimitiveTools`, `UEditorAppToolset` | `content-world.md` |
| Blueprint classes and graphs | `BlueprintTools` | `AssetTools`, `ObjectTools`, `ActorTools` | `blueprint.md` |
| Materials | `MaterialTools` | `MaterialInstanceTools`, `AssetTools`, `TextureTools` | `material.md` |
| PCG | `UPCGToolset` | `SceneTools`, `AssetTools` | `pcg.md` |
| Niagara systems | `UNiagaraToolset_System` | `_Assets`, `_Component`, `_Blueprint`, `_Info`, `AssetTools` | `niagara.md` |
| UMG | `UUMGToolSet` | `ObjectTools`, `BlueprintTools`, `AssetTools` | `umg.md` |
| Sequencer and Control Rig | `SequencerTools` | `SequencerKeyframingTools`, `SequencerControlRigTools`, `ControlRigTools` | Search catalog first |
| Skeletal/static meshes | `SkeletalMeshTools` or `StaticMeshTools` | `PhysicsAssetToolset`, `AssetTools` | Search catalog first |
| GAS and Gameplay Tags | `UAbilitySystemInspectorToolset` | `UAttributeSetToolset`, `UGameplayCueToolset`, `UGameplayTagsToolset` | Search catalog first |
| AI data | `BehaviorTreeTools` or `StateTreeTools` | `ConversationTools`, `UWorldConditionTools` | Search catalog first |
| Data assets and tables | `DataAssetTools` or `DataTableTools` | `CurveTableTools`, `StringTableTools`, `UDataRegistryTools` | Search catalog first |
| Plugins and config | `UPluginToolset` | `UConfigSettingsToolset`, `UGameFeaturesToolset` | Search catalog first |
| Dataflow and cloth | `UDataflowAgentToolset` | `UChaosClothAssetToolset` | Search catalog and bundled UE skill |
| Editor UI automation | `USlateInspectorToolset` | Direct domain Toolset first | Use only when no direct API exists |
| Logs and visual checks | `ULogsToolset` | `UEditorAppToolset`, `USlateInspectorToolset` | `diagnostics.md` |
| Tests and C++ compile | `UAutomationTestToolset` | `ULiveCodingToolset`, `ULogsToolset` | `diagnostics.md` |

## Routing Rules

- Prefer semantic/domain APIs to Slate clicking.
- Use `ObjectTools.list_properties` before property reads/writes whenever the class is unfamiliar. This is mandatory for UMG widget and slot objects.
- Use `AssetTools` for discovery, editability, referencers, saving, and dirty-state checks.
- Use `UEditorAppToolset` for selection, camera, screenshots, open editors, and PIE.
- Use `ULogsToolset` after compilation, execution, or any call that can fail asynchronously.
- Search `kind=skill` for engine-provided durable workflows, but treat live schemas as authoritative for callable details.
