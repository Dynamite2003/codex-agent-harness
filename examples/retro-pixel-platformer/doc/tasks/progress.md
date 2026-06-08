# Retro Pixel Platformer Task Progress

## 目标

基于 `doc/proposal.md` 和 `doc/detailed-design.md`，将原创复古像素横版平台跳跃游戏 MVP 拆分为最小可执行、可验证的模块任务。任务优先按端到端垂直切片推进，确保每个阶段都能形成可运行或可测试的增量。

## 输入

- 需求文档：`doc/proposal.md`
- 详细设计文档：`doc/detailed-design.md`
- 需求 spec：`doc/specs/2026-06-08-retro-pixel-platformer.md`
- 当前项目：greenfield 浏览器游戏项目

## 输出

- [app-shell-boot.md](./app-shell-boot.md)
- [input.md](./input.md)
- [game-state-manager.md](./game-state-manager.md)
- [level-system.md](./level-system.md)
- [physics-collision.md](./physics-collision.md)
- [entity-system.md](./entity-system.md)
- [scoring-lives.md](./scoring-lives.md)
- [game-loop.md](./game-loop.md)
- [renderer.md](./renderer.md)
- [hud-overlay-ui.md](./hud-overlay-ui.md)

## 步骤

1. 先实现可启动、可销毁、可测试的浏览器入口。
2. 再实现输入、状态、关卡和初始数据契约。
3. 然后实现物理碰撞、实体交互、计分生命和主循环。
4. 最后实现像素渲染、HUD/Overlay、端到端验证和人工原创/IP 审查。

## 模块进度 Checklist

- [x] `AFK` App Shell / Boot：创建浏览器入口、配置装配、生命周期控制。Trace: EARS Runtime & Presentation；ADR-002、ADR-003；AC Browser Runtime。
- [x] `AFK` Input：实现键盘动作映射、持续输入、边沿触发和销毁监听。Trace: EARS Input；ADR-004；AC Controls、Level Completion。
- [x] `AFK` Game State Manager：实现 `booting`、`playing`、`win`、`lose` 和重开状态恢复。Trace: EARS Game States；ADR-005、ADR-009；AC Level Completion、UI State。
- [x] `AFK` Level System：定义原创单关卡、tile grid、实体初始数据、边界、危险区和终点。Trace: EARS Level & Movement、Enemies；ADR-001、ADR-006、ADR-008；AC Browser Runtime、Level Completion。
- [x] `AFK` Physics & Collision：实现 AABB、tile 阻挡、重力、落地、无二段跳和 stomp 分类。Trace: EARS Level & Movement、Input、Enemies；ADR-007、ADR-008；AC Controls、Enemies & Lives。
- [x] `AFK` Entity System：实现玩家、敌人、收集物、危险区、终点实体更新和重置。Trace: EARS Collectibles & Scoring、Enemies；ADR-006、ADR-008；AC Collectibles & Score、Enemies & Lives。
- [x] `AFK` Scoring & Lives：实现分数、3 条生命、扣命、失败和 run 重置规则。Trace: EARS Collectibles & Scoring、Enemies, Damage, Lives；ADR-009；AC Collectibles & Score、Enemies & Lives。
- [x] `AFK` Game Loop：实现固定步长、RAF 驱动、状态门控、渲染调用和后台恢复保护。Trace: EARS Game States；ADR-007；AC Level Completion、UI State。
- [x] `AFK` Renderer：实现原创像素风格关卡/实体/HUD 绘制、摄像机和 nearest-neighbor 缩放。Trace: EARS Runtime & Presentation；ADR-001、ADR-003；AC Browser Runtime、UI State。
- [ ] `AFK complete / HITL pending` HUD / Overlay UI：已实现分数生命、胜利失败和重开提示；人工可读性与原创/IP 审查仍待确认。Trace: EARS Runtime & Presentation、Game States；ADR-001、ADR-005；AC UI State、Browser Runtime。

## 推荐执行顺序

1. App Shell / Boot
2. Input
3. Game State Manager
4. Level System
5. Physics & Collision
6. Entity System
7. Scoring & Lives
8. Game Loop
9. Renderer
10. HUD / Overlay UI

## 可并行项

- Input 可与 Level System 并行，只需共享 `InputState` 和 `LevelDefinition` 契约。
- Renderer 的基础绘制可与 Game Loop 并行，只需共享 `GameState` 和 `RenderSurface` 契约。
- HUD / Overlay UI 的文案和状态可见性可在 Game State Manager 后并行推进。

## 阻塞项

- 没有当前会影响任务划分的阻塞问题。
- `HITL` 原创/IP 审查必须在最终验收前完成，因为 ADR-001 是明确约束。
- 如实现阶段决定更换技术栈或引入第三方素材，需要先确认许可、原创性和是否改变 ADR。

## 总体验收标准

- 浏览器打开入口后无需 native 安装即可进入可玩关卡。
- 键盘左右移动、跳跃、无二段跳、收集、敌人 stomp/伤害、危险区扣命、终点胜利、生命耗尽失败和 `R` 重开均可验证。
- 分数、生命、胜利、失败状态在画面中清晰可见。
- 所有角色、敌人、收集物、tile、终点、名称和关卡布局均保持原创，不出现可识别商业 IP。
