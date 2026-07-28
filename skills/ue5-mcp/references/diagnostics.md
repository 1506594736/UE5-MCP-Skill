# Diagnostics And Validation

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
