<div align="center">

# UE5 MCP Skill

**让 Codex 通过 Unreal Engine 5.8.1 内置 MCP 检查、修改并验证编辑器内容**

[![Unreal Engine 5.8.1](https://img.shields.io/badge/Unreal_Engine-5.8.1-0E1128?logo=unrealengine&logoColor=white)](https://www.unrealengine.com/)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-111111)](skills/ue5-mcp/SKILL.md)
[![MCP 2025-11-25](https://img.shields.io/badge/MCP-2025--11--25-2563EB)](https://modelcontextprotocol.io/)
[![Validate catalog](https://github.com/1506594736/UE5-MCP-Skill/actions/workflows/validate.yml/badge.svg)](https://github.com/1506594736/UE5-MCP-Skill/actions/workflows/validate.yml)

一个面向实际 UE 编辑器操作的低上下文 Codex Skill。它不把完整工具目录一次性塞进提示词，而是先本地检索候选工具，再以运行中的 UE MCP Schema 为最终依据。

[快速开始](#快速开始) · [工作原理](#工作原理) · [能力范围](#能力范围) · [安全与验证](#安全与验证) · [项目状态](#项目状态)

</div>

---

## 项目定位

这个仓库只包含一个 Skill：[`ue5-mcp`](skills/ue5-mcp/SKILL.md)。

它解决的不是“让模型背下全部 UE API”，而是让 Codex 在连接实时 Unreal Editor 后，按照稳定的工程流程完成任务：

```text
检查当前状态
    -> 检索候选 Toolset
    -> 获取运行时 Schema
    -> 执行最小范围修改
    -> 编译与保存
    -> 日志、结构或画面验证
```

核心原则：

- **运行时优先**：`describe_toolset` 返回的实时 Schema 高于本地快照和模型记忆。
- **低上下文检索**：本地 JSON 由脚本搜索，完整工具目录不会进入模型上下文。
- **先读后写**：修改 Blueprint、资产、Actor、属性或图表前先检查现状。
- **结果必须验证**：成功的 MCP 调用不等于任务成功，必须编译、保存并读回。
- **控制破坏范围**：删除、重命名、替换、重设父类等操作必须有清晰授权范围。

## 快速开始

### 1. 前置条件

- Unreal Engine 5.8.1。
- UE 项目已启用 `ModelContextProtocol` 和任务需要的 Toolset 插件。
- Unreal Editor 已打开目标项目，并启动 MCP HTTP 服务。
- 已安装 Codex。

Codex 连接 UE 不需要额外安装 `MCPClientToolset`。它是 UE 作为 MCP 客户端时使用的组件，不是 Codex 调用 UE 的必需项。

### 2. 安装 Skill

```powershell
git clone https://github.com/1506594736/UE5-MCP-Skill.git
Copy-Item -Recurse -Force `
  .\UE5-MCP-Skill\skills\ue5-mcp `
  "$HOME\.codex\skills\ue5-mcp"
```

### 3. 配置 MCP

在 `~/.codex/config.toml` 中添加：

```toml
[mcp_servers.unreal-mcp]
url = "http://127.0.0.1:8000/mcp"
```

重新启动 Codex 后检查连接：

```powershell
codex mcp list
```

预期能看到：

```text
unreal-mcp  http://127.0.0.1:8000/mcp  enabled
```

### 4. 第一次调用

建议先执行只读检查：

```text
使用 $ue5-mcp，连接当前运行的 UE5.8.1 编辑器。
检查当前关卡、已选 Actor 和最近的错误日志，只读取，不做修改。
```

确认连接正常后再执行编辑任务：

```text
使用 $ue5-mcp，检查 /Game/Blueprints/BP_Door 的 Event Graph。
在不破坏现有逻辑的前提下增加开门事件，完成后编译、保存并读取错误日志。
```

## 工作原理

```text
用户的 UE 任务
      |
      v
Codex 加载 SKILL.md
      |
      +----> router.md 识别 Blueprint / PCG / Niagara / UMG 等领域
      |
      +----> search_tools.py 搜索本地清洗目录
      |           |
      |           v
      |      Bundled catalog snapshot（统计由脚本读取）
      |
      v
list_toolsets -> describe_toolset -> call_tool
      |
      v
运行中的 Unreal Editor
      |
      v
Compile -> Save -> Logs / Readback / Screenshot / PIE
```

### 分层加载

| 层级 | 内容 | 何时进入上下文 |
|---|---|---|
| Metadata | Skill 名称和触发描述 | Codex 启动后用于自动发现 |
| `SKILL.md` | 路由、执行纪律、验证要求 | Skill 触发时 |
| Domain References | Blueprint、PCG、Niagara、UMG 等工作流 | 当前任务需要时 |
| Tool Catalog | 清洗后的 JSON 快照 | 不直接加载，由脚本检索 |
| Live Schema | 当前 UE 实例的真实参数结构 | 调用 `describe_toolset` 时 |

本地目录只负责快速找到候选工具。工具是否存在、运行时完整名称、参数名称、枚举值和对象结构，始终以当前编辑器为准。

## 能力范围

| 领域 | 主要能力 | 最低验证要求 |
|---|---|---|
| Blueprint | 类、变量、事件、函数、节点、Pin、Graph DSL | 编译、图结构读回、保存 |
| Content / World | 资产、Actor、组件、关卡、属性、编辑器状态 | 属性读回、脏状态和保存检查 |
| Material | Material、Material Function、Material Instance | 重编译、连接检查、画面检查 |
| PCG | Graph、Node、Pin、参数、实例执行 | Graph 结构、Data View、日志 |
| Niagara | System、Emitter、Module、Renderer、User Parameter | Compile State、Stack Issues、画面检查 |
| UMG | Widget Blueprint、Widget Tree、Slot、事件绑定 | Widget 编译、属性读回、布局截图 |
| Diagnostics | UE 日志、截图、PIE、Automation Test、Live Coding | 对应结果和错误报告 |

更完整的领域路由见 [`references/router.md`](skills/ue5-mcp/references/router.md)。

## 安全与验证

Skill 默认采用以下证据顺序：

```text
1. 运行时 describe_toolset Schema
2. MCP 返回值和对象/属性检查
3. 本地清洗工具目录
4. 领域工作流文档
5. 模型已有知识
```

### 修改任务的完成标准

| 修改类型 | 不能只看 | 必须补充 |
|---|---|---|
| 属性修改 | `call_tool` 返回成功 | 再次读取属性并比较目标值 |
| Blueprint / UMG | 节点或控件已创建 | 编译、读取错误、保存资产 |
| Material | 表达式已连接 | 重编译并检查资产或视口画面 |
| PCG / Niagara | Graph 或 Stack 已更新 | 执行/编译状态、输出或画面检查 |
| C++ | Live Coding 返回成功 | 编译诊断和实际编辑器/PIE 行为 |

高风险操作包括资产删除、批量重命名、Widget 替换、Blueprint 重设父类和文件覆盖。执行前应检查依赖与 Referencer，并确保用户请求明确覆盖该范围。

## 工具目录

工具快照的引擎版本、生成时间和统计数据记录在 `references/toolsets/_index.json` 中，用于候选工具检索，不是运行时 Schema 的替代品。不要在文档中复制这些版本敏感数据；使用 `search_tools.py --stats` 读取当前统计。

在 Skill 目录中执行搜索：

```powershell
cd .\skills\ue5-mcp
python .\scripts\search_tools.py "compile blueprint" --limit 8 --format minimal
python .\scripts\search_tools.py "user variables" --toolset UNiagaraToolset_System --format minimal
python .\scripts\search_tools.py --kind skill "material"
python .\scripts\validate_knowledge.py
python .\scripts\validate_knowledge.py --max-age 90
python .\scripts\validate_knowledge.py --editor-version 5.8.1
```

工具发现优先使用 `--format minimal`，它只输出签名或记录 ID；需要候选描述时省略该参数，需要完整结构化记录时使用 `--json`。

如果系统 Python 不可用，可以使用 UE 自带的 Python：

```powershell
& "<UE_ROOT>\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" `
  .\scripts\search_tools.py "compile blueprint" --limit 8 --format minimal
```

## 仓库结构

```text
UE5-MCP-Skill/
├── README.md
└── skills/
    └── ue5-mcp/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── scripts/
        │   ├── search_tools.py
        │   └── validate_knowledge.py
        └── references/
            ├── router.md
            ├── blueprint.md
            ├── content-world.md
            ├── material.md
            ├── pcg.md
            ├── niagara.md
            ├── umg.md
            ├── diagnostics.md
            ├── failure-patterns.md
            └── toolsets/
```

## 项目状态

当前版本定位为可用的低上下文 V1，Skill 格式、目录数据和 MCP 三件套已经验证。运行时 Toolset 注册名和启用状态会随 UE 构建及项目插件变化，因此每次会话仍需以 `list_toolsets` 和 `describe_toolset` 为权威来源。

下一阶段重点：

- 建立本地短名到运行时完整 Toolset 名称的映射。
- 建立自动化的运行时目录同步和快照更新流程。
- 增加不上传 GitHub 的项目配置文件。
- 完成 Blueprint、Material、PCG、Niagara、UMG 的隔离资产端到端测试。
