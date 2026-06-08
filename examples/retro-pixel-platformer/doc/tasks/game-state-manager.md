# Game State Manager

## 模块目标

实现 `booting`、`playing`、`win`、`lose` 状态机，统一管理 run 初始化、胜利、失败和重开。重开必须从关卡初始数据重建状态，避免玩家、敌人、收集物、分数、生命或摄像机残留。

## 依赖输入

- `doc/proposal.md`：EARS Game States、Enemies, Damage, Lives；Acceptance Criteria / Level Completion、UI State。
- `doc/detailed-design.md`：模块 4 Game State Manager、游戏状态机、ADR-005、ADR-009。
- 依赖契约：`GameState`、`LevelDefinition`、`GameConfig`、`createInitialGameState()`。

## Out of Scope

- 不实现输入监听、物理碰撞或渲染 overlay。
- 不设计菜单、暂停、设置或存档状态。
- 不改变初始 3 条生命和直接进入关卡的 MVP 契约。

## 任务 Checklist

- [x] `AFK` 定义 `GameStatus` 和状态转换辅助函数。Trace: EARS Game States；Design Game State Machine。
- [x] `AFK` 实现 `startRun()`，从 `booting` 进入 `playing` 并使用关卡初始状态。Trace: ADR-005；AC Browser Runtime。
- [x] `AFK` 实现 `enterWin()`，只允许从 `playing` 且玩家存活时进入 `win`。Trace: EARS Level & Movement；AC Level Completion。
- [x] `AFK` 实现 `enterLose()`，生命归零时进入 `lose`。Trace: EARS Enemies, Damage, Lives；AC Enemies & Lives。
- [x] `AFK` 实现 `restartRun()`，从 `win` / `lose` 回到全新 `playing` run。Trace: EARS Input、Game States；AC Level Completion。
- [x] `AFK` 确保 `win` / `lose` 状态下普通玩法更新不会改变玩家、敌人、分数和生命。Trace: Data Invariants；AC Level Completion。
- [x] `AFK` 补充状态机单元测试，覆盖非法转换、胜利、失败、重开和初始状态恢复。Trace: Testing Strategy / State Manager。

## 验收标准

- 初始启动后状态可进入 `playing`。
- 玩家到达终点时状态进入 `win`，并停止普通玩法推进。
- 生命归零时状态进入 `lose`，并停止普通玩法推进。
- `win` 或 `lose` 时触发重开会恢复玩家位置、敌人、收集物、分数、生命、摄像机和状态。

## 测试要求

- 单元测试：状态转换、状态门控、重开重置。
- 集成测试：与 Input、Scoring & Lives、Level System 组合验证胜负和重开。

## AFK/HITL 标记

- `AFK`：状态机、重置和测试可独立实现。
- `HITL`：如需加入菜单、暂停、检查点或存档，必须确认是否扩大 MVP。

## Blocked by

- 依赖 Level System 提供 `createInitialGameState()` 的最终契约。
- 可在 Level System 完成前用最小测试关卡推进。

## 可能修改的文件范围

- `src/state/*`
- `src/level/*`
- `src/types/*`
- `tests/game-state-manager.*`
