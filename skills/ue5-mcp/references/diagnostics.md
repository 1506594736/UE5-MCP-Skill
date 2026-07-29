# Diagnostics And Validation

## Validation Levels

### Fast

Use Fast by default for isolated, routine, narrowly scoped mutations.

1. Run the domain compile, recompile, or execution check once when the change requires it. Count a documented built-in compile as that compile.
2. Re-read only the exact properties, graph subgraph, connections, parameters, or component structure changed and compare them with the request.
3. Read focused error or warning entries when the operation is asynchronous, its result is ambiguous, or the domain Toolset does not return structured diagnostics.
4. Save the exact modified assets and confirm they are no longer dirty where supported.

### Full

Use Full when the user requests runtime proof, the change affects visual or runtime behavior, the target is shared or high-risk, the change spans multiple assets, or Fast evidence is ambiguous.

1. Complete all Fast checks.
2. Re-read the broader affected structure, dependencies, and related state.
3. Capture and inspect relevant logs from a baseline.
4. Capture an asset or viewport image when appearance matters.
5. Run PIE when runtime behavior must be observed, then stop PIE and confirm it stopped.
6. Run focused automation tests for broad or risky changes when suitable tests exist.

Validation levels add to the selected domain reference; they do not replace its minimum evidence. Do not run images, PIE, or automation tests merely because Full was selected when that evidence cannot validate the requested outcome.

## Logs

1. Capture a baseline timestamp or recent log position.
2. Perform the operation.
3. Read new entries with `ULogsToolset.GetLogEntries`, filtering by relevant category or severity when supported.
4. Report errors and actionable warnings; do not bury them in raw log volume.

## Images

- Use `CaptureAssetImage` for an asset-editor result.
- Use `CaptureViewport` for scene appearance and runtime results.
- Use `CaptureEditorImage` only when the full editor UI matters.
- Capture before and after visual changes. Verify that the returned image is nonblank and shows the intended target.

## PIE

1. Confirm PIE is not already running.
2. Start PIE and wait for the intended state.
3. Inspect logs, actors, runtime components, or screenshots.
4. Stop PIE and confirm it stopped.

## Automation Tests

1. Call `DiscoverTests` once per session.
2. Use `ListTests` or a focused filter.
3. Run only the relevant tests.
4. Poll status when needed and retrieve results.
5. Include failing test names, errors, warnings, and durations in the report.

## Live Coding

Use `CompileLiveCoding` only when Live Coding is enabled and the code change is compatible with it. Read the complete compiler diagnostics. A successful compile does not validate Blueprint wiring, asset state, or runtime behavior; perform the matching editor/runtime check afterward.

## Minimum Evidence

| Change | Required evidence |
|---|---|
| Property | Readback equals intended value |
| Asset graph | Structure readback plus compile/recompile |
| Blueprint/UMG | Successful compile plus saved clean asset |
| PCG/Niagara | Successful execution/compile state plus output or visual check |
| Runtime logic | PIE observation plus relevant logs |
| C++ | Compiler result plus editor/runtime validation |
