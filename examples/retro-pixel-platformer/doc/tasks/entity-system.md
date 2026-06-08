# Entity System

## 模块目标

实现玩家、敌人、收集物、危险区域和终点实体的状态管理、更新入口和交互响应。实体系统需要支持从关卡初始数据恢复，保证重开 run 后实体不会残留旧状态。

## 依赖输入

- `doc/proposal.md`：EARS Collectibles & Scoring、Enemies, Damage, Lives、Level & Movement；Acceptance Criteria / Collectibles & Score、Enemies & Lives、Level Completion。
- `doc/detailed-design.md`：模块 7 Entity System、实体类型、收集物流程、敌人交互流程、终点流程。
- 依赖契约：`PlayerState`、`EnemyState`、`CollectibleState`、`HazardState`、`GoalState`。

## Out of Scope

- 不实现最终 sprite 美术。
- 不实现分数和生命的持久化或 HUD 展示。
- 不创建多敌人类型或复杂 AI。

## 任务 Checklist

- [x] `AFK` 定义实体状态类型和从 `LevelDefinition` 克隆实体的工厂函数。Trace: Design Data Model；ADR-006。
- [x] `AFK` 实现玩家状态更新入口，接收输入意图和物理结果后更新位置、速度、朝向、grounded、短暂无敌计时。Trace: EARS Input、Level & Movement；AC Controls。
- [x] `AFK` 实现 patroller 敌人的最小巡逻更新，在巡逻范围边界反向。Trace: EARS Enemies, Damage, Lives；AC Enemies & Lives。
- [x] `AFK` 实现收集物碰撞处理：未收集时标记 `collected = true`。Trace: EARS Collectibles & Scoring；AC Collectibles & Score。
- [x] `AFK` 实现敌人被 stomp 后 `alive = false`，失效敌人不再造成伤害。Trace: EARS Enemies, Damage, Lives；AC Enemies & Lives。
- [x] `AFK` 实现危险区和跌落区域检测，向 Scoring & Lives 发出扣命意图。Trace: EARS Enemies, Damage, Lives；AC Enemies & Lives。
- [x] `AFK` 实现终点重叠检测，向 Game State Manager 发出胜利意图。Trace: EARS Level & Movement；AC Level Completion。
- [x] `AFK` 补充实体集成测试，覆盖收集、敌人巡逻、stomp、侧面接触、危险区和终点。Trace: Testing Strategy / Enemy Interaction、Integration。

## 验收标准

- 收集物被玩家触碰后从 active 碰撞和渲染状态中移除。
- alive 敌人可巡逻；被 stomp 后失效且不再造成伤害。
- 非 stomp 敌人接触、危险区或跌落能触发扣命流程。
- 玩家接触终点且仍存活时触发胜利。
- 重开 run 后所有实体恢复到关卡初始状态。

## 测试要求

- 单元测试：实体工厂、敌人巡逻、收集物状态、敌人失效状态。
- 集成测试：与 Physics & Collision、Scoring & Lives、Game State Manager 组合验证完整交互。

## AFK/HITL 标记

- `AFK`：实体状态、交互和测试可独立完成。
- `HITL`：如新增敌人造型、命名或行为表达，需要原创/IP 审查。

## Blocked by

- 依赖 Level System 提供实体初始数据。
- 依赖 Physics & Collision 提供玩家/敌人重叠和 stomp 分类。
- 依赖 Scoring & Lives 提供计分和扣命函数。

## 可能修改的文件范围

- `src/entities/*`
- `src/level/*`
- `src/state/*`
- `src/physics/*`
- `src/types/*`
- `tests/entity-system.*`
