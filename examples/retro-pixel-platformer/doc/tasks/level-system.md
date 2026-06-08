# Level System

## 模块目标

定义至少一个原创横版平台关卡，并提供关卡加载、初始状态创建、solid tile 查询、实体初始数据、关卡边界、失败区域和终点区域。该模块是玩法垂直切片的基础数据源。

## 依赖输入

- `doc/proposal.md`：EARS Level & Movement、Collectibles & Scoring、Enemies, Damage, Lives；ADR Candidates 001、004、005。
- `doc/detailed-design.md`：模块 5 Level System、Level 契约、ADR-001、ADR-006、ADR-008。
- 依赖数据模型：`LevelDefinition`、`GameState`、`Rect`、实体 state 类型。

## Out of Scope

- 不实现物理求解、实体 AI、渲染或美术最终 polish。
- 不创建多个关卡、关卡选择或关卡编辑器。
- 不使用第三方素材、商业 IP 名称、可识别角色或经典关卡布局复刻。

## 任务 Checklist

- [x] `AFK` 定义 `LevelDefinition`、tile id、关卡尺寸和 `tileSize` 契约。Trace: Design Data Model；ADR-008。
- [x] `AFK` 创建原创 MVP 关卡数据，包含起点、地面、平台、风险区域、收集物、敌人和终点。Trace: EARS Level & Movement；ADR-006；AC Level Completion。
- [x] `AFK` 实现 `loadLevel(id)`，返回已知关卡并处理未知 id。Trace: Design Level Contract；AC Browser Runtime。
- [x] `AFK` 实现 `createInitialGameState(level, config)`，从关卡数据创建玩家、敌人、收集物、危险区、终点、分数、生命和摄像机初始状态。Trace: ADR-009；AC Level Completion。
- [x] `AFK` 实现 `isSolidAt(level, tileX, tileY)`，关卡外按阻挡或边界规则处理。Trace: EARS Level & Movement；AC Controls。
- [x] `AFK` 实现 `querySolidTiles(level, bounds)`，为 AABB 碰撞返回相关 solid tile 矩形。Trace: ADR-008；AC Controls。
- [x] `AFK` 补充关卡数据测试，验证关卡包含所有 MVP 元素且终点理论可达。Trace: AC Level Completion、Collectibles & Score、Enemies & Lives。
- [ ] `HITL` 执行关卡布局原创/IP 审查，确认没有复刻可识别商业 IP 关卡节奏或标志性组合。Trace: ADR-001；AC Browser Runtime。

## 验收标准

- 至少一个关卡包含起点、可 traversable 平台、收集物、敌人、风险区域和终点。
- `createInitialGameState()` 生成的 state 满足 `score >= 0`、`lives = 3`、实体状态完整。
- solid tile 查询能支持玩家站立、撞墙和头顶碰撞。
- 关卡命名、布局和实体概念均为原创。

## 测试要求

- 单元测试：关卡加载、未知 id、solid 查询、初始状态创建。
- 集成测试：从起点到终点存在可验证路径；关卡中至少有一个收集物、一个敌人、一个危险区。
- 人工验收：视觉/IP 审查关卡组合和名称。

## AFK/HITL 标记

- `AFK`：数据契约、关卡定义和自动测试可独立完成。
- `HITL`：原创/IP 审查需要人工确认。

## Blocked by

- 无当前阻塞。
- 如果实现阶段要使用外部 tileset 或 sprite pack，需先确认许可和 ADR-001 合规性。

## 可能修改的文件范围

- `src/level/*`
- `src/state/*`
- `src/types/*`
- `tests/level-system.*`
