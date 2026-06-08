# Retro Pixel Platformer Implementation Prompt

## 目标

你是实现阶段的新对话 agent。不要依赖任何需求、设计或任务拆分阶段的聊天历史；只能使用本 prompt 明确列出的输入和 artifact。

基于现有规划 artifact，实现原创复古像素横版平台跳跃游戏 MVP。游戏必须能在浏览器运行，支持键盘移动、跳跃、收集物、敌人交互、计分、生命、胜利、失败和重开，并严格避免使用超级马里奥、任天堂或任何可识别商业 IP 的名称、角色、素材、关卡布局、logo、视觉组合或 trade dress。

默认采用单 agent 顺序执行。按 `doc/tasks/progress.md` 的推荐顺序推进模块，实现代码、运行验证、更新 checklist，直到 MVP 可运行且主要验收标准可验证。

## 输入

- 需求文档：`doc/proposal.md`
- 详细设计：`doc/detailed-design.md`
- 任务目录：`doc/tasks/`
- 总体进度：`doc/tasks/progress.md`
- 模块任务：
  - `doc/tasks/app-shell-boot.md`
  - `doc/tasks/input.md`
  - `doc/tasks/game-state-manager.md`
  - `doc/tasks/level-system.md`
  - `doc/tasks/physics-collision.md`
  - `doc/tasks/entity-system.md`
  - `doc/tasks/scoring-lives.md`
  - `doc/tasks/game-loop.md`
  - `doc/tasks/renderer.md`
  - `doc/tasks/hud-overlay-ui.md`
- Spec artifact：
  - `doc/specs/index.md`
  - `doc/specs/2026-06-08-retro-pixel-platformer.md`
- 当前项目目录：`/Users/bytedance/Documents/Programs/Vibe2Spec/examples/retro-pixel-platformer`

## 输出

- 可运行的浏览器游戏 MVP 代码。
- 按任务完成情况更新后的 `doc/tasks/<module-name>.md`。
- 按总体进度更新后的 `doc/tasks/progress.md`。
- 如实现采用设计中已收敛但 spec 尚未同步的默认契约，回填相关 spec；如代码实现偏离 spec、ADR 或 Acceptance Criteria，必须回填相关文档或记录偏离原因。
- 最终报告，包含完成项、关键文件、验证命令与结果、未验证风险、spec 回填或偏离记录。

## 执行规则

1. 先阅读 `doc/proposal.md`、`doc/detailed-design.md`、`doc/specs/` 和 `doc/tasks/`，再检查现有代码结构、配置文件和工具链。
2. 先识别现有技术栈和可用工具，再决定实现方式和验证命令。不要为静态 Web、无依赖项目或已有项目强行引入不存在的 `uv`、`pytest`、`mypy`、`ruff`、`npm`、`node`。
3. 当前规划显示这是 greenfield 浏览器游戏项目。若仓库仍无现有源码或包管理配置，优先考虑能直接运行的最小浏览器实现；只有确有测试、构建或维护收益时才引入依赖或包管理配置，并说明理由。
4. 严格遵守 Spec、ADR 和 Acceptance Criteria。尤其遵守 ADR-001 原创 IP 边界、ADR-002 浏览器本地单页游戏、ADR-003 Canvas 风格渲染契约、ADR-004 键盘优先、ADR-007 固定步长逻辑更新、ADR-008 Tile + AABB 碰撞、ADR-009 三条生命和重开规则。
5. 不要回滚用户已有改动。遇到无关脏文件保持不动；遇到影响实现的改动，先理解并在当前基础上工作。
6. 默认单 agent 顺序推进，不强制并行，不强制启用多个 subagents。
7. 只有当任务彼此独立、文件范围清晰、预计单 agent 上下文会明显过长时，才允许可选启用子 agents。启用前必须先声明：
   - 每个子 agent 的文件所有权。
   - 合并顺序。
   - 冲突处理策略。
   - 共享契约文件如何只由一个 owner 修改。
8. 每个模块必须根据对应的 `doc/tasks/<module-name>.md` 实现代码、补充 focused tests 或等价验证，并把完成状态回写到该模块 checklist 和 `doc/tasks/progress.md`。
9. 对 `HITL` 项，如果无法获得人工确认，记录为未验证风险；不要假装已完成人工原创/IP 审查。
10. 不引入服务端、账号、联网、移动触控、音频、标题菜单、设置页、排行榜、多关卡或长期存档，除非相关 artifact 已明确要求。

## 步骤

1. 读取输入 artifact，整理 MVP 行为、数据契约、ADR、Acceptance Criteria、任务顺序和阻塞项。
2. 检查仓库现状，确认是否已有源码、测试、构建脚本、运行入口和包管理配置。
3. 选择与仓库匹配的最小实现技术栈。若无依赖静态 Web 足够，不要为了测试或构建强行创建复杂工具链。
4. 按 `doc/tasks/progress.md` 推荐顺序实现：
   - App Shell / Boot
   - Input
   - Game State Manager
   - Level System
   - Physics & Collision
   - Entity System
   - Scoring & Lives
   - Game Loop
   - Renderer
   - HUD / Overlay UI
5. 每完成一个模块，更新对应 `doc/tasks/<module-name>.md` 的 checklist；完成总体模块后更新 `doc/tasks/progress.md`。
6. 实现时保持模块契约可测试：
   - `bootstrapGame(root, config?)`
   - `createKeyboardInput(target)`
   - `updateGame(state, input, dt, level, config)`
   - `loadLevel(id)`
   - `createInitialGameState(level, config)`
   - `isSolidAt(level, tileX, tileY)`
   - `querySolidTiles(level, bounds)`
   - `intersects(a, b)`
   - `classifyEnemyContact(player, previousPlayer, enemy)`
   - `renderGame(state, surface)`
7. 实现至少一个原创可玩关卡，包含起点、平台、收集物、敌人、风险区域和终点。关卡布局、命名、角色、敌人、tile、收集物、终点和 UI 表达必须原创。
8. 确保核心玩法满足：
   - `ArrowLeft` / `KeyA` 左移。
   - `ArrowRight` / `KeyD` 右移。
   - `ArrowUp` / `KeyW` / `Space` 跳跃。
   - 仅 grounded 时允许跳跃，不允许未确认的二段跳。
   - `KeyR` 在 `win` / `lose` 状态重开。
   - 收集物加 100 分并从 active 状态移除。
   - 从上方 stomp 敌人加 200 分并使敌人失效。
   - 非 stomp 接触敌人、危险区或跌落扣 1 条生命。
   - 初始 3 条生命；扣命后仍有生命则回到关卡起点，保留当前 run 的分数和已收集状态。
   - 生命归零进入 `lose`。
   - 到达终点进入 `win`。
   - `win` / `lose` 状态停止普通玩法推进，但允许重开。
9. 实现像素风格渲染、HUD 和 overlay。画面应非空、清晰、nearest-neighbor 或等价像素缩放；HUD 显示分数和生命；胜利/失败 overlay 清楚且提示 `R` 重开。
10. 对照 `doc/detailed-design.md` 的 Spec 回填要求，判断是否需要更新 `doc/specs/2026-06-08-retro-pixel-platformer.md` 和 `doc/specs/index.md`。如不回填，说明原因；如实现偏离，记录偏离原因和影响。

## 测试与验证

1. 优先沿用仓库现有测试命令和工具配置。先检查 README、配置文件、脚本和 package metadata，再运行命令。
2. Python 项目优先沿用仓库现有测试命令。只有已经 bootstrap-python，或项目已有 `uv` / `pytest` / `mypy` / `ruff` 配置时，才使用：
   - `uv run pytest`
   - `uv run mypy`
   - `uv run ruff check .`
3. Node 或前端项目只有在存在或新建了合理的 `package.json` 时，才根据实际脚本运行 `test`、`lint`、`typecheck`、`build`。不要假设脚本存在。
4. 静态 Web 或无依赖前端项目至少执行以下验证中的可用项：
   - 契约测试：验证输入、状态机、关卡、碰撞、计分生命、重开等纯逻辑契约。
   - 源码级逻辑测试：用可用运行时直接执行核心模块测试，或编写最小测试 harness。
   - DOM smoke：验证入口元素、canvas/HUD/overlay 存在。
   - 浏览器截图验证：确认页面非空、HUD 可见、像素画面正常、无明显文字重叠或布局错位。
5. 如果浏览器、运行时或测试工具不可用，必须记录不可用原因、已尝试命令和替代验证。
6. 手测或自动验证至少覆盖：
   - 浏览器打开入口无需 native 安装即可进入可玩关卡。
   - 左右移动、跳跃、撞墙、落地、无二段跳。
   - 收集物消失并加分。
   - 从上方 stomp 敌人加分，侧面接触敌人扣生命。
   - 危险区或跌落扣生命，生命耗尽失败。
   - 到达终点胜利。
   - 胜利或失败后按 `R` 重开，分数、生命、实体和玩家位置恢复初始状态。
   - 分数、生命、胜利、失败状态可见。
   - 命名、视觉、关卡和 UI 不出现可识别商业 IP。

## 进度更新

- 每完成一个模块，立即更新对应 `doc/tasks/<module-name>.md` checklist。
- 每完成一个总体模块，更新 `doc/tasks/progress.md`。
- checklist 中未完成项保持未勾选，不要为了收尾虚假标记。
- 阻塞项写明原因、已尝试方案、影响范围和需要用户提供的信息。
- `HITL` 原创/IP 审查如果没有人工确认，保留为风险或待确认项。

## 最终报告

最终回复必须包含：

1. 完成项：列出已完成模块和关键行为。
2. 关键文件：列出主要新增或修改文件。
3. 验证命令与结果：逐条列出运行过的命令、结果和失败原因。
4. 未验证风险：说明无法验证的浏览器、运行时、HITL、IP 审查或手感风险。
5. Spec 回填或偏离记录：说明已更新哪些 spec / ADR / Acceptance Criteria 相关文档；如未更新或发生偏离，说明原因。
6. 本地运行方式：说明如何在当前项目中打开或启动游戏。
