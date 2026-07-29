# UMG Workflow

## Inspect Or Create

1. List or find Widget Blueprints before creating a new asset.
2. Call `GetWidgets`, `GetNamedSlots`, `GetWidgetDescription`, and `GetWidgetTreeDepth` as appropriate.
3. Query widget classes and class information before adding a widget.

## Mandatory Property Sequence

For every returned Widget and Slot object:

1. Call `ObjectTools.list_properties`.
2. Call `ObjectTools.get_properties` with exact discovered names.
3. Call `ObjectTools.set_properties` with exact discovered names.
4. Read back changed values.

Property names vary by widget and slot class. Guessing can silently set the wrong property or do nothing.

## Edit And Validate

1. Add, move, wrap, rename, or bind widgets while preserving returned references.
2. Ensure widgets required by event binding or C++ `BindWidget` are variables with compatible classes.
3. Treat widget replacement reports as required review output; resolve unmatched referenced members.
4. Compile once after the hierarchy, properties, and bindings are complete.
5. Inspect compile errors and re-read the changed tree. Capture the editor/asset view when layout or appearance matters, then save separately through `AssetTools`.

Do not use visible text to infer slot ownership or property names. Do not replace a widget or panel merely to work around an unknown property; inspect the actual widget and slot classes first.
