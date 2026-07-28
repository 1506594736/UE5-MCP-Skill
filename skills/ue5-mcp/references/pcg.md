# PCG Workflow

## Inspect Or Create

1. Find an existing graph before creating one.
2. Read graph description, structure, parameters, and graph schema.
3. Call `ListNativeNodes` or `ListAvailableSubgraphs`, then query `GetNativeNodeSchema` for the selected node type.
4. Never infer settings fields or pin names from display labels.

## Edit

1. Add nodes with stable names and clear positions.
2. Configure nodes through the schema returned by the live Toolset.
3. Connect exact source and destination pins.
4. Re-read node info and graph structure after each coherent topology batch.
5. Use graph parameters for values that should vary between instances.

## Execute And Validate

1. List existing graph instances before spawning a new one.
2. Set instance parameters, execute the intended instance, and collect its result.
3. Inspect graph structure and `GetNodeDataView` for the relevant output node.
4. Check the UE log for PCG errors or warnings.
5. Save the graph and affected level/actor assets.

Do not spawn duplicate graph instances merely to test an existing placed instance. Confirm whether execution is editor-time or runtime and whether deterministic seed behavior matters.
