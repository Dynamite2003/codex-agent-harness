# Physics & Collision

## 模块目标

实现平台跳跃所需的基础物理和 AABB 碰撞：重力、速度积分、水平/垂直 tile 阻挡、落地状态、边界限制、无二段跳，以及玩家和敌人的 stomp / damage 分类。

## 依赖输入

- `doc/proposal.md`：EARS Input、Level & Movement、Enemies, Damage, Lives；Acceptance Criteria / Controls、Enemies & Lives。
- `doc/detailed-design.md`：模块 6 Physics & Collision、Collision 契约、跳跃流程、敌人交互流程、ADR-007、ADR-008。
- 依赖契约：`KinematicBody`、`CollisionResult`、`PlayerState`、`EnemyState`、`LevelDefinition`。

## Out of Scope

- 不实现完整物理引擎、斜坡、多边形碰撞或像素级碰撞。
- 不实现敌人 AI、分数增减、生命扣减或渲染。
- 不加入二段跳、冲刺、蹬墙或复杂动作。

## 任务 Checklist

- [x] `AFK` 实现 `intersects(a, b)` 和基础 rect 工具函数。Trace: Design Collision Contract；ADR-008。
- [x] `AFK` 实现重力和最大下落速度应用。Trace: EARS Level & Movement；ADR-007；AC Controls。
- [x] `AFK` 实现水平速度积分和 solid tile 水平碰撞修正。Trace: EARS Level & Movement；AC Controls。
- [x] `AFK` 实现垂直速度积分、落地、头顶碰撞和 `grounded` 设置。Trace: EARS Level & Movement；AC Controls。
- [x] `AFK` 实现跳跃资格判断：仅 `jumpPressed && grounded` 时设置向上速度。Trace: EARS Input；AC Controls。
- [x] `AFK` 验证 airborne 时重复跳跃不会重置上升速度。Trace: EARS Input；AC Controls。
- [x] `AFK` 实现 `classifyEnemyContact(player, previousPlayer, enemy)`，使用上一帧底部、当前重叠和下落速度识别 stomp。Trace: Enemy Interaction Flow；AC Enemies & Lives。
- [x] `AFK` 补充碰撞单元测试，覆盖撞墙、落地、顶撞、无二段跳、stomp 和侧面 damage。Trace: Testing Strategy / Physics & Collision。

## 验收标准

- 玩家不能穿过 solid tile 或关卡边界。
- 玩家下落到有效表面后 `grounded = true`，跳跃后 `grounded = false`。
- 空中按跳跃键不会产生未确认的二段跳。
- 从上方下落接触敌人分类为 `stomp`；侧面或非下落接触分类为 `damage`。

## 测试要求

- 单元测试：AABB 相交、tile 查询集成、水平/垂直碰撞、grounded、无二段跳、stomp 分类。
- 集成测试：玩家在测试关卡中左右移动、跳跃、撞墙、落地和踩踏敌人。

## AFK/HITL 标记

- `AFK`：碰撞算法和自动测试可独立完成。
- `HITL`：如需要调优手感参数到产品偏好，需要人工试玩确认。

## Blocked by

- 依赖 Level System 提供 solid tile 查询和关卡边界。
- 依赖 Entity System 的实体尺寸契约保持一致。

## 可能修改的文件范围

- `src/physics/*`
- `src/collision/*`
- `src/entities/*`
- `src/types/*`
- `tests/physics-collision.*`
