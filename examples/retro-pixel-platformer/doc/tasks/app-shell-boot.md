# App Shell / Boot

## 模块目标

创建浏览器游戏入口和生命周期编排，使实现 agent 能从空项目启动一个可挂载、可销毁、可测试的本地单页游戏。该模块只负责装配配置、关卡、输入、状态、主循环和渲染容器，不实现具体玩法规则。

## 依赖输入

- `doc/proposal.md`：EARS Runtime & Presentation、Input、Game States；Acceptance Criteria / Browser Runtime。
- `doc/detailed-design.md`：模块 1 App Shell / Boot、API / App 契约、ADR-002、ADR-003。
- 依赖后续模块契约：`GameConfig`、`LevelDefinition`、`GameController`、`InputController`、`renderGame`。

## Out of Scope

- 不实现具体物理、敌人 AI、计分规则或关卡内容。
- 不引入服务端、账号、联网、移动触控或音频。
- 不创建标题菜单或设置页。

## 任务 Checklist

- [x] `AFK` 搭建最小浏览器入口和根容器挂载流程，输出可加载的游戏 screen。Trace: EARS Runtime & Presentation；ADR-002；AC Browser Runtime。
- [x] `AFK` 定义 `GameConfig` 默认值，包括逻辑分辨率、tile 尺寸、重力、速度、生命和分值。Trace: ADR-007、ADR-009；AC Controls、Enemies & Lives。
- [x] `AFK` 实现 `bootstrapGame(root, config?)`，装配配置、关卡初始状态、输入控制器和主循环控制器。Trace: Design App Contract；AC Browser Runtime。
- [x] `AFK` 实现 `GameController.startRun()`、`restartRun()`、`destroy()`、`getState()` 的最小可测试行为。Trace: Design App Contract；AC Level Completion。
- [x] `AFK` 确保 `destroy()` 清理键盘监听、动画帧和 DOM/canvas 资源。Trace: Design App Contract；Testing Strategy / Input。
- [x] `AFK` 增加启动冒烟测试，验证入口可重复挂载、销毁后不再推进状态。Trace: AC Browser Runtime；Testing Strategy / State Manager。

## 验收标准

- 在桌面浏览器或测试环境挂载入口后，存在游戏渲染容器且初始状态进入 `playing`。
- `bootstrapGame` 可重复调用，不污染其他测试实例。
- 调用 `destroy()` 后，动画循环停止，输入监听被移除。
- 模块不包含商业 IP 名称、素材引用或关卡复刻内容。

## 测试要求

- 单元测试：`bootstrapGame` 返回控制器、默认配置合并、`getState()` 只读语义。
- 集成测试：挂载后进入 `playing`，销毁后状态不继续变化。
- 浏览器验证：入口页面可打开，无 native 安装要求。

## AFK/HITL 标记

- `AFK`：入口、配置、控制器和测试均可由 agent 独立完成。
- `HITL`：仅当实现阶段选择非设计文档技术栈或外部托管方式时需要人工确认。

## Blocked by

- 无当前阻塞。
- 被 `Level System` 的 `loadLevel()` 和 `createInitialGameState()` 契约实现质量影响，但可先用 stub 推进。

## 可能修改的文件范围

- `package.json`
- `index.html`
- `src/main.*`
- `src/app/*`
- `src/config/*`
- `src/types/*`
- `tests/app-shell-boot.*`
