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
2. Call `GetNodeDataView` for the intended instance and output node before execution. On the first call this enables inspection; an error indicating that no inspection data exists is expected.
3. Set instance parameters, call `ExecuteGraphInstance` for that instance, and wait for its asynchronous result to complete.
4. Call `GetNodeDataView` again for the same instance, node, and output pin, then verify the returned data against the request.
5. Re-read graph structure and instance parameters, and check the UE log for PCG errors or warnings.
6. Save the graph and affected level/actor assets.

Inspection state is shared by the graph asset. When multiple actors use the same graph, complete the enable-inspection -> execute -> data-view sequence for one actor before starting the next; concurrent calls can freeze the editor.

Do not spawn duplicate graph instances merely to test an existing placed instance. Confirm whether execution is editor-time or runtime and whether deterministic seed behavior matters.
