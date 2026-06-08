# Input

## 模块目标

实现键盘输入控制器，将物理按键转换为语义动作：`moveLeft`、`moveRight`、`jumpDown`、`jumpPressed`、`restartPressed`。输入必须支持持续状态和单帧边沿触发，并可在销毁时移除监听。

## 依赖输入

- `doc/proposal.md`：EARS Input；Acceptance Criteria / Controls、Level Completion。
- `doc/detailed-design.md`：模块 3 Input、Input 契约、ADR-004。
- 依赖数据契约：`InputState`。

## Out of Scope

- 不实现可重绑定键位、触控、鼠标或手柄。
- 不实现暂停、菜单导航或设置页。
- 不决定物理移动速度或跳跃高度。

## 任务 Checklist

- [x] `AFK` 定义 `InputState` 和 `InputController` 类型或等价 JSDoc 结构。Trace: Design Input Contract；ADR-004。
- [x] `AFK` 实现 `createKeyboardInput(target)`，监听 `keydown` 和 `keyup`。Trace: EARS Input；AC Controls。
- [x] `AFK` 映射左移为 `ArrowLeft` / `KeyA`，右移为 `ArrowRight` / `KeyD`。Trace: ADR-004；AC Controls。
- [x] `AFK` 映射跳跃为 `ArrowUp` / `KeyW` / `Space`，并区分 `jumpDown` 与 `jumpPressed`。Trace: EARS Input；AC Controls。
- [x] `AFK` 映射重开为 `KeyR`，输出单帧 `restartPressed`。Trace: EARS Input、Game States；AC Level Completion。
- [x] `AFK` 实现 `afterFrame()`，清除 `jumpPressed` 和 `restartPressed` 的边沿触发状态。Trace: Design Input Contract；Testing Strategy / Input。
- [x] `AFK` 实现 `destroy()`，移除所有事件监听。Trace: Design Input Contract；App Contract。
- [x] `AFK` 补充键盘输入单元测试，覆盖按下、释放、重复 keydown、边沿触发和销毁。Trace: Testing Strategy / Input。

## 验收标准

- 按住左/右移动键时，`moveLeft` 或 `moveRight` 持续为 `true`，释放后为 `false`。
- 首次按下跳跃键的帧 `jumpPressed = true`，调用 `afterFrame()` 后变为 `false`，按住期间 `jumpDown = true`。
- 首次按下 `R` 的帧 `restartPressed = true`，后续帧不重复触发，直到重新按下。
- `destroy()` 后继续触发键盘事件不会改变输入状态。

## 测试要求

- 单元测试：键位映射、边沿触发、持续状态、重复按键、销毁监听。
- 集成测试：与 Game State Manager 组合验证 `win` / `lose` 状态下按 `R` 可重开。

## AFK/HITL 标记

- `AFK`：全部输入契约和测试可由 agent 独立完成。
- `HITL`：仅当产品要求更改默认键位或加入可重绑定时需要确认。

## Blocked by

- 无当前阻塞。
- 与 App Shell / Boot 的挂载目标有关，但可用 `window` 或测试 DOM 独立完成。

## 可能修改的文件范围

- `src/input/*`
- `src/types/*`
- `tests/input.*`
