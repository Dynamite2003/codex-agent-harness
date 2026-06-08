# HUD / Overlay UI

## 模块目标

实现游戏状态反馈：`playing` 时显示分数和生命，`win` 时显示明确胜利状态和重开提示，`lose` 时显示明确失败状态和重开提示。UI 需要与像素风格一致、可读、不遮挡核心玩法，并保持原创表达。

## 依赖输入

- `doc/proposal.md`：EARS Runtime & Presentation、Game States；Acceptance Criteria / UI State、Level Completion。
- `doc/detailed-design.md`：模块 10 HUD / Overlay UI、状态机、ADR-001、ADR-005。
- 依赖契约：`GameState.status`、`score`、`lives`、`restartPressed`。

## Out of Scope

- 不实现标题页、设置页、暂停菜单、键位重绑定或长期存档 UI。
- 不引入营销落地页或说明型 onboarding。
- 不加入音频、触控或社交功能。

## 任务 Checklist

- [x] `AFK` 在 `playing` 状态绘制或显示分数。Trace: EARS Runtime & Presentation；AC UI State。
- [x] `AFK` 在 `playing` 状态绘制或显示生命数量。Trace: EARS Runtime & Presentation；AC UI State。
- [x] `AFK` 在 `win` 状态显示清晰胜利信息，并提示按 `R` 重开。Trace: EARS Game States；ADR-005；AC UI State、Level Completion。
- [x] `AFK` 在 `lose` 状态显示清晰失败信息，并提示按 `R` 重开。Trace: EARS Game States；ADR-005；AC UI State、Level Completion。
- [x] `AFK` 确保 `win` / `lose` overlay 不继续显示普通玩法误导性状态变化。Trace: Game State Invariants；AC Level Completion。
- [x] `AFK` 验证 HUD 不随摄像机滚动，且在常见桌面窗口尺寸下不遮挡玩家关键区域。Trace: Renderer Contract；AC UI State。
- [x] `AFK` 补充 UI 状态测试，覆盖 playing、win、lose、重开提示可见。Trace: Testing Strategy / Browser Verification。
- [ ] `HITL` 人工审查 UI 文案、图形和状态表达是否原创且不使用商业 IP 名称或可识别 trade dress。Trace: ADR-001；AC Browser Runtime。

## 验收标准

- `playing` 状态下分数和生命始终可见。
- 胜利后出现明确胜利状态，普通玩法推进停止，按 `R` 可重新开始。
- 失败后出现明确失败状态，普通玩法推进停止，按 `R` 可重新开始。
- HUD 和 overlay 文字在桌面浏览器中可读，不与核心玩法画面严重重叠。
- UI 表达原创，不使用受限商业 IP 名称或素材。

## 测试要求

- 单元或组件测试：不同 `GameState.status` 下输出正确 HUD/overlay 状态。
- 集成测试：win/lose 后移动输入不推进，`R` 重开。
- 浏览器验证：HUD 可读、overlay 清晰、无明显重叠。
- 人工验收：UI 原创/IP 审查。

## AFK/HITL 标记

- `AFK`：HUD/overlay 状态逻辑和自动测试可独立完成。
- `HITL`：最终文案和视觉原创/IP 审查需要人工确认。

## Blocked by

- 依赖 Renderer 提供绘制或 UI 容器能力。
- 依赖 Game State Manager 提供状态门控和重开行为。

## 可能修改的文件范围

- `src/ui/*`
- `src/rendering/*`
- `src/state/*`
- `src/styles/*`
- `tests/hud-overlay-ui.*`
