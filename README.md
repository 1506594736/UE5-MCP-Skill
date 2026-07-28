# UE5 MCP Skill

A low-context Codex Skill for operating Unreal Engine 5 through the engine's Model Context Protocol server.

The repository contains one Skill at `skills/ue5-mcp`. It routes Unreal tasks to live MCP Toolsets, searches a bundled catalog of UE 5.8 tools without loading the catalog into model context, and requires compile/save/log/visual validation after editor changes.

## Install

Copy `skills/ue5-mcp` into your Codex skills directory:

```powershell
Copy-Item -Recurse -Force .\skills\ue5-mcp "$HOME\.codex\skills\ue5-mcp"
```

Configure the Unreal MCP server in `~/.codex/config.toml`:

```toml
[mcp_servers.unreal-mcp]
url = "http://127.0.0.1:8000/mcp"
```

Restart Codex, open the Unreal project with the MCP server enabled, then invoke the Skill explicitly with `$ue5-mcp` or let its UE task triggers load it automatically.

## Knowledge Snapshot

The bundled cleaned snapshot contains 26 plugins, 55 Toolsets, 865 tools, and 12 engine-provided workflow Skills. Run `scripts/search_tools.py` for focused lookup and `scripts/validate_knowledge.py` to verify the snapshot.
