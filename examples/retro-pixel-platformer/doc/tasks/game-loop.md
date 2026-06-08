# Game Loop

## 模块目标

实现 `requestAnimationFrame` 驱动的主循环和固定步长逻辑更新。循环需要读取输入、根据状态门控推进玩法、限制后台恢复后的累计更新次数，并调用渲染而不让渲染修改状态。

## 依赖输入

- `doc/proposal.md`：EARS Game States、Runtime & Presentation；Acceptance Criteria / Level Completion、UI State。
- `doc/detailed-design.md`：模块 2 Game Loop、每帧更新流程、Game Loop 契约、ADR-007。
- 依赖契约：`updateGame()`、`renderGame()`、`InputController`、`GameState`、`GameConfig`。

## Out of Scope

- 不实现具体碰撞、实体规则或 HUD 样式。
- 不引入 Web Worker、服务端同步或复杂性能系统。
- 不实现暂停菜单。

## 任务 Checklist

- [x] `AFK` 实现固定步长 accumulator，逻辑更新以秒为单位接收 `dt`。Trace: ADR-007；AC Controls。
- [x] `AFK` 使用 `requestAnimationFrame` 驱动循环，并记录/取消 animation frame id。Trace: EARS Runtime & Presentation；AC Browser Runtime。
- [x] `AFK` 实现单帧过长保护，限制最大累计更新次数或最大 delta。Trace: Design Game Loop；Risk / 浏览器帧率风险。
- [x] `AFK` 在每帧读取输入，并在帧尾调用 `input.afterFrame()`。Trace: Design Frame Flow；AC Controls。
- [x] `AFK` 在 `playing` 状态推进物理、实体、计分、摄像机和目标检测。Trace: EARS Game States；AC Level Completion。
- [x] `AFK` 在 `win` / `lose` 状态停止普通玩法推进，但保留重开输入。Trace: EARS Game States；AC Level Completion。
- [x] `AFK` 调用 `renderGame(readonlyState, surface)`，并确保渲染层不修改状态。Trace: Game Loop Contract；AC UI State。
- [x] `AFK` 补充主循环测试，使用 fake RAF 或直接调用 step 验证固定步长、状态门控和销毁。Trace: Testing Strategy / Integration。

## 验收标准

- 不同显示刷新率下逻辑更新保持可预测。
- 浏览器后台恢复或长帧不会导致玩家穿透、瞬移或一次推进过多状态。
- `win` / `lose` 后移动输入不再推进普通玩法，`R` 仍可重开。
- 主循环销毁后不会继续调度 RAF。

## 测试要求

- 单元测试：accumulator、长帧限制、销毁。
- 集成测试：`playing` 推进状态，`win` / `lose` 只渲染和接受重开。
- 浏览器验证：入口运行后动画持续刷新，无明显卡死。

## AFK/HITL 标记

- `AFK`：主循环和自动测试可独立完成。
- `HITL`：如需基于实际手感调整固定步长或最大更新次数，需要人工试玩确认。

## Blocked by

- 依赖 App Shell / Boot 装配入口。
- 依赖 Input、Game State Manager、Physics & Collision、Entity System、Scoring & Lives 的 update 契约。
- 可先用空 update 和 mock render 测试循环本身。

## 可能修改的文件范围

- `src/game-loop/*`
- `src/app/*`
- `src/state/*`
- `src/input/*`
- `src/rendering/*`
- `tests/game-loop.*`
