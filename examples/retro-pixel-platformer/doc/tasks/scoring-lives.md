# Scoring & Lives

## 模块目标

实现当前 run 的分数和生命规则：收集物加 100 分、stomp 敌人加 200 分、初始 3 条生命、受伤扣命、生命归零失败、仍有剩余生命时玩家回到关卡起点且当前 run 的分数和已收集状态保留。

## 依赖输入

- `doc/proposal.md`：EARS Collectibles & Scoring、Enemies, Damage, Lives、Game States；Acceptance Criteria / Collectibles & Score、Enemies & Lives。
- `doc/detailed-design.md`：模块 8 Scoring & Lives、生命损失流程、MVP 契约、ADR-009。
- 依赖契约：`GameState`、`GameConfig`、`PlayerState`、`CollectibleState`、`EnemyState`。

## Out of Scope

- 不实现排行榜、长期存档、成就或关卡间累计分数。
- 不设计 UI 文案或 HUD 布局。
- 不改变 3 条生命、100/200 分值和回到起点的 MVP 默认契约。

## 任务 Checklist

- [x] `AFK` 定义分数和生命操作函数：`addCollectibleScore`、`addStompScore`、`loseLife` 或等价接口。Trace: EARS Collectibles & Scoring；ADR-009。
- [x] `AFK` 实现收集物加分，默认每个收集物加 100。Trace: EARS Collectibles & Scoring；AC Collectibles & Score。
- [x] `AFK` 实现 stomp 敌人加分，默认每个敌人加 200。Trace: EARS Collectibles & Scoring；AC Collectibles & Score。
- [x] `AFK` 实现非 stomp 敌人接触、危险区和跌落扣 1 条生命。Trace: EARS Enemies, Damage, Lives；AC Enemies & Lives。
- [x] `AFK` 实现生命剩余时玩家回到关卡起点、清空速度、设置短暂无敌，保留分数和已收集状态。Trace: ADR-009；AC Enemies & Lives。
- [x] `AFK` 实现生命归零进入 `lose` 状态。Trace: EARS Enemies, Damage, Lives；AC Enemies & Lives。
- [x] `AFK` 实现完整 restart run 时分数、生命、敌人、收集物和玩家状态恢复初始值。Trace: EARS Game States；AC Level Completion。
- [x] `AFK` 补充分数生命测试，覆盖加分、扣命、失败、重开和状态保留。Trace: Testing Strategy / Scoring & Lives。

## 验收标准

- 收集物碰撞后 score 增加 100。
- stomp 敌人后 score 增加 200。
- 受伤后 lives 减少；如果 lives 仍大于 0，玩家回到起点且当前 run 分数与已收集状态保留。
- lives 减到 0 时状态进入 `lose`。
- `restartRun()` 后 score 回到 0，lives 回到 3，收集物和敌人恢复初始状态。

## 测试要求

- 单元测试：加分、扣命、归零失败、剩余生命重置玩家。
- 集成测试：收集物、敌人、危险区、跌落和重开组合流程。

## AFK/HITL 标记

- `AFK`：分数生命规则和测试可独立完成。
- `HITL`：如产品要调整生命数、分值或 respawn 规则，需要人工确认。

## Blocked by

- 依赖 Game State Manager 的 `enterLose()` 和 `restartRun()`。
- 依赖 Entity System 触发收集、stomp、伤害和跌落事件。

## 可能修改的文件范围

- `src/scoring/*`
- `src/state/*`
- `src/entities/*`
- `src/config/*`
- `src/types/*`
- `tests/scoring-lives.*`
