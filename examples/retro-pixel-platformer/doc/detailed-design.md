# Retro Pixel Platformer Detailed Design

## 目标

根据 `doc/proposal.md` 生成可进入实现阶段的详细设计文档，覆盖模块边界、数据模型、关键流程、本地契约、ADR、验收标准映射、风险和测试策略。

## 输入

- 需求文档：`doc/proposal.md`
- 独立需求 spec：`doc/specs/2026-06-08-retro-pixel-platformer.md`
- Spec 索引：`doc/specs/index.md`
- 当前项目状态：greenfield 浏览器游戏项目，未发现业务源码、README 或包管理配置。

## 输出

- 本设计文档：`doc/detailed-design.md`

## 步骤

1. 读取需求文档和现有 spec，确认已明确需求、非目标、ADR Candidates 和验收标准。
2. 将需求拆分为运行时、输入、游戏循环、物理碰撞、关卡、实体、UI 状态和原创资产边界等模块。
3. 将需求阶段 ADR Candidates 收敛为明确设计 ADR。
4. 定义后续实现可遵守的本地数据契约、状态机和关键流程。
5. 将验收标准映射到可实现、可测试的设计点。
6. 记录风险、测试策略和可能需要同步的 spec 文件。

## Context

这是一个 greenfield 浏览器游戏 MVP。设计阶段不依赖其他聊天历史，只基于 `doc/proposal.md` 和 `doc/specs/2026-06-08-retro-pixel-platformer.md`。

游戏是一款原创复古像素横版平台跳跃游戏。玩家通过键盘控制原创角色移动、跳跃、收集物品、处理敌人并到达终点。系统必须提供计分、生命、胜利、失败和重开能力，并且不得使用超级马里奥、任天堂或任何可识别商业 IP 的角色、名称、素材、关卡布局、logo 或 trade dress。

需求文档包含若干开放问题。为避免阻塞 MVP 设计，本设计只收敛对核心验收必要且不会扩大产品范围的默认契约：桌面键盘优先、直接进入可玩关卡、3 条生命、生命损失后回到关卡起点、无音频、无触控和联网能力。它们是设计阶段的 MVP 决策，不代表后续不能调整。

## Goals & Non-Goals

### Goals

- 提供一个能在桌面浏览器运行的单人离线 MVP 架构。
- 支持一个完整可玩关卡，包含起点、平台、收集物、敌人、风险区域和终点。
- 支持键盘移动、跳跃、无二段跳的基础平台跳跃手感。
- 支持 AABB 碰撞、重力、实体交互、计分、生命、胜利、失败和重开。
- 保持所有视觉元素、命名、关卡布局和行为表达为原创。
- 让验收标准能映射到后续实现任务和测试用例。

### Non-Goals

- 不设计多人、联网、排行榜、账号、云存档、广告或社交分享。
- 不要求移动触控、手柄、可重绑定按键或复杂辅助功能。
- 不要求音效、音乐、暂停菜单、标题菜单、设置页或关卡编辑器。
- 不要求多关卡、程序生成关卡、长期存档或成就系统。
- 不复刻任何可识别商业 IP 的角色轮廓、敌人造型、道具、命名、关卡节奏或视觉 trade dress。
- 不在本阶段生成任务清单或修改业务代码。

## 模块划分

### 1. App Shell / Boot

职责：

- 创建浏览器游戏入口、画布或渲染容器。
- 初始化游戏配置、关卡数据、输入监听、状态管理器和主循环。
- 处理浏览器窗口尺寸变化下的像素画面缩放。

边界：

- 不包含具体物理、关卡规则或实体行为。
- 只负责生命周期编排。

### 2. Game Loop

职责：

- 使用 `requestAnimationFrame` 驱动渲染。
- 使用固定步长更新游戏逻辑，避免不同刷新率导致核心行为漂移。
- 在 `playing` 状态推进物理、碰撞、AI 和计分。
- 在 `win` / `lose` 状态暂停普通玩法推进，但保留重开输入。

关键契约：

- 逻辑更新以秒为单位接收 `dt`。
- 单帧过长时限制最大累计更新次数，避免浏览器后台恢复后状态跳变。

### 3. Input

职责：

- 监听键盘按下和释放。
- 将物理按键转换为语义动作：`moveLeft`、`moveRight`、`jumpPressed`、`restartPressed`。
- 区分持续动作和单次触发动作。

默认键位：

- 左移：`ArrowLeft` / `KeyA`
- 右移：`ArrowRight` / `KeyD`
- 跳跃：`ArrowUp` / `KeyW` / `Space`
- 重开：`KeyR`，仅在 `win` 或 `lose` 状态必需响应。

### 4. Game State Manager

职责：

- 管理游戏状态：`booting`、`playing`、`win`、`lose`。
- 暴露 `startRun()`、`restartRun()`、`enterWin()`、`enterLose()`。
- 统一重置玩家、关卡实体、分数、生命和摄像机。

状态边界：

- `playing` 是唯一推进普通玩法的状态。
- `win` 和 `lose` 只允许 UI overlay、渲染和重开输入。

### 5. Level System

职责：

- 定义至少一个横版关卡的数据。
- 管理 tile grid、实体初始位置、关卡边界、失败区域和终点区域。
- 提供碰撞查询和摄像机跟随范围。

关卡组成：

- 起点：玩家初始生成点。
- 固体平台：地面、浮动平台、边界。
- 收集物：至少一种原创收集物。
- 敌人：至少一种原创敌人。
- 风险区域：例如坑洞或伤害区域。
- 终点：到达后进入胜利状态。

### 6. Physics & Collision

职责：

- 对玩家和移动敌人应用速度、重力和位置积分。
- 使用 AABB 处理实体与 solid tile 的碰撞。
- 计算 `grounded` 状态，限制跳跃只在站立于有效表面时触发。
- 识别玩家与敌人、收集物、危险区域、终点的重叠。

碰撞规则：

- 水平移动遇到固体 tile 时停止穿透。
- 垂直下落遇到固体 tile 时落地并设置 `grounded = true`。
- 垂直上升撞到固体 tile 时停止上升。
- 玩家底部从上方接触敌人顶部，且玩家垂直速度向下时，判定为 stomp。

### 7. Entity System

职责：

- 管理玩家、敌人、收集物、危险区域和终点实体。
- 将实体更新、碰撞响应和渲染状态分离。
- 支持重开时从关卡初始数据恢复实体。

实体类型：

- `Player`：位置、速度、生命、朝向、grounded、短暂无敌计时。
- `Enemy`：位置、速度、巡逻范围、存活状态。
- `Collectible`：位置、分值、是否已收集。
- `Hazard`：伤害区域或失败区域。
- `Goal`：终点触发区域。

### 8. Scoring & Lives

职责：

- 管理当前 run 的分数和生命。
- 收集物和 stomp 敌人增加分数。
- 非 stomp 敌人接触、伤害区域或跌出关卡造成生命损失。
- 生命归零进入 `lose`。

MVP 契约：

- 初始生命：3。
- 收集物分数：100。
- stomp 敌人分数：200。
- 生命损失但仍有剩余生命时，玩家回到关卡起点，分数和已收集物状态保持当前 run 状态。
- 重开 run 时，玩家位置、敌人、收集物、分数、生命、摄像机和状态全部恢复到初始值。

### 9. Renderer

职责：

- 渲染像素风格关卡、实体、HUD 和状态 overlay。
- 使用整数缩放或 nearest-neighbor 规则保持像素边缘清晰。
- 摄像机跟随玩家，但不显示关卡边界外区域。

原创视觉边界：

- 角色、敌人、收集物、tile、终点和 UI icon 必须使用原创外观。
- 禁止使用或临摹可识别商业 IP 的颜色组合、轮廓、敌人造型、管道/砖块/旗杆等标志性组合。

### 10. HUD / Overlay UI

职责：

- 在 `playing` 状态显示分数、生命和必要状态反馈。
- 在 `win` 状态显示明确胜利信息和重开提示。
- 在 `lose` 状态显示明确失败信息和重开提示。

边界：

- MVP 不包含独立标题页或设置页；打开后直接进入可玩关卡。

## 数据模型

以下为本地契约模型，后续实现可用 TypeScript 类型、JSDoc 或等价结构表达。

```ts
type GameStatus = "booting" | "playing" | "win" | "lose";

type Vector2 = {
  x: number;
  y: number;
};

type Rect = {
  x: number;
  y: number;
  width: number;
  height: number;
};

type GameConfig = {
  logicalWidth: number;
  logicalHeight: number;
  tileSize: number;
  gravity: number;
  maxFallSpeed: number;
  playerMoveSpeed: number;
  playerJumpSpeed: number;
  startingLives: number;
  collectibleScore: number;
  stompScore: number;
};

type InputState = {
  moveLeft: boolean;
  moveRight: boolean;
  jumpDown: boolean;
  jumpPressed: boolean;
  restartPressed: boolean;
};

type GameState = {
  status: GameStatus;
  score: number;
  lives: number;
  levelId: string;
  player: PlayerState;
  enemies: EnemyState[];
  collectibles: CollectibleState[];
  hazards: HazardState[];
  goal: GoalState;
  camera: CameraState;
};

type PlayerState = {
  id: "player";
  position: Vector2;
  velocity: Vector2;
  size: Vector2;
  spawnPoint: Vector2;
  facing: "left" | "right";
  grounded: boolean;
  invulnerableSeconds: number;
};

type EnemyState = {
  id: string;
  kind: "patroller";
  position: Vector2;
  velocity: Vector2;
  size: Vector2;
  patrolMinX: number;
  patrolMaxX: number;
  alive: boolean;
};

type CollectibleState = {
  id: string;
  position: Vector2;
  size: Vector2;
  scoreValue: number;
  collected: boolean;
};

type HazardState = {
  id: string;
  bounds: Rect;
  kind: "damage" | "fall";
};

type GoalState = {
  bounds: Rect;
};

type CameraState = {
  position: Vector2;
  viewport: Vector2;
};

type KinematicBody = {
  position: Vector2;
  previousPosition: Vector2;
  velocity: Vector2;
  size: Vector2;
  grounded: boolean;
};

type CollisionResult = {
  body: KinematicBody;
  hitLeft: boolean;
  hitRight: boolean;
  hitCeiling: boolean;
  hitGround: boolean;
};

type LevelDefinition = {
  id: string;
  name: string;
  widthTiles: number;
  heightTiles: number;
  tileSize: number;
  playerSpawn: Vector2;
  solidTiles: number[][];
  enemies: Omit<EnemyState, "alive">[];
  collectibles: Omit<CollectibleState, "collected">[];
  hazards: HazardState[];
  goal: GoalState;
};
```

数据不变量：

- `score >= 0`。
- `lives >= 0`。
- `player.grounded` 只能由物理碰撞结果设置。
- `collected = true` 的收集物不再参与碰撞或渲染。
- `alive = false` 的敌人不再造成伤害。
- `status = win | lose` 时普通玩法更新不再改变玩家、敌人、分数和生命。

## 状态机或关键流程

### 游戏状态机

```text
booting
  -> playing

playing
  -> win   : 玩家存活并接触终点
  -> lose  : 生命归零

win
  -> playing : 玩家触发重开

lose
  -> playing : 玩家触发重开
```

状态行为：

- `booting`：加载配置和关卡定义，构造初始状态。
- `playing`：读取输入、更新物理、处理碰撞、更新敌人和摄像机、渲染 HUD。
- `win`：停止普通玩法推进，渲染胜利 overlay，等待重开。
- `lose`：停止普通玩法推进，渲染失败 overlay，等待重开。

### 每帧更新流程

```text
readInput()
  -> if status is win/lose and restartPressed: restartRun()
  -> if status is not playing: renderOnly()
  -> updatePlayerIntent()
  -> applyGravity()
  -> integrateHorizontal()
  -> resolveHorizontalTileCollision()
  -> integrateVertical()
  -> resolveVerticalTileCollisionAndGrounded()
  -> updateEnemies()
  -> resolvePlayerCollectibles()
  -> resolvePlayerEnemyInteractions()
  -> resolvePlayerHazardsAndFalls()
  -> resolveGoal()
  -> updateCamera()
  -> render()
```

### 跳跃流程

```text
GIVEN status = playing
WHEN jumpPressed = true and player.grounded = true
THEN player.velocity.y = -playerJumpSpeed and player.grounded = false

GIVEN player.grounded = false
WHEN jumpPressed = true
THEN do not start another jump
```

### 敌人交互流程

```text
IF player overlaps alive enemy:
  IF player is descending AND previousPlayerBottom <= enemyTop + stompTolerance:
    enemy.alive = false
    player.velocity.y = -stompBounceSpeed
    score += stompScore
  ELSE IF player is not invulnerable:
    loseLife()
```

### 生命损失流程

```text
loseLife():
  lives -= 1
  IF lives <= 0:
    enterLose()
  ELSE:
    reset player to level spawn
    clear player velocity
    set short invulnerability window
```

### 收集物流程

```text
IF player overlaps collectible AND collectible.collected = false:
  collectible.collected = true
  score += collectible.scoreValue
```

### 终点流程

```text
IF status = playing AND lives > 0 AND player overlaps goal:
  enterWin()
```

## API / 本地契约

本项目没有服务端 API。所有契约均为浏览器本地模块契约。

### App 契约

```ts
function bootstrapGame(root: HTMLElement, config?: Partial<GameConfig>): GameController;

type GameController = {
  startRun(): void;
  restartRun(): void;
  destroy(): void;
  getState(): Readonly<GameState>;
};
```

约束：

- `bootstrapGame` 必须可重复用于测试环境挂载。
- `destroy` 必须移除键盘监听和动画循环。
- `getState` 用于测试和调试，不应允许外部直接修改状态。

### Input 契约

```ts
function createKeyboardInput(target: Window | HTMLElement): InputController;

type InputController = {
  read(): InputState;
  afterFrame(): void;
  destroy(): void;
};
```

约束：

- `jumpPressed` 和 `restartPressed` 是边沿触发，只在按下帧为 `true`。
- `moveLeft` / `moveRight` / `jumpDown` 是持续状态。

### Game Loop 契约

```ts
function updateGame(state: GameState, input: InputState, dt: number, level: LevelDefinition, config: GameConfig): GameState;
function renderGame(state: Readonly<GameState>, surface: RenderSurface): void;
```

约束：

- `updateGame` 应保持可测试性；同一输入状态和 `dt` 应得到确定性结果。
- 渲染不应修改游戏状态。

### Level 契约

```ts
function loadLevel(id: string): LevelDefinition;
function createInitialGameState(level: LevelDefinition, config: GameConfig): GameState;
function isSolidAt(level: LevelDefinition, tileX: number, tileY: number): boolean;
function querySolidTiles(level: LevelDefinition, bounds: Rect): Rect[];
```

约束：

- 关卡定义必须是原创数据。
- `createInitialGameState` 是重开 run 的唯一状态来源，避免局部重置遗漏。

### Collision 契约

```ts
function intersects(a: Rect, b: Rect): boolean;
function resolveActorVsTiles(actor: KinematicBody, level: LevelDefinition, dt: number): CollisionResult;
function classifyEnemyContact(player: PlayerState, previousPlayer: PlayerState, enemy: EnemyState): "stomp" | "damage" | "none";
```

约束：

- stomp 判定必须同时参考当前重叠、上一帧玩家底部位置和玩家下落速度。
- 不能只用重叠方向推断 stomp，否则侧面碰撞容易误判。

### Rendering 契约

```ts
type RenderSurface = {
  clear(): void;
  drawTile(tileId: number, x: number, y: number): void;
  drawSprite(spriteId: string, x: number, y: number, flipX?: boolean): void;
  drawText(text: string, x: number, y: number): void;
};
```

约束：

- 画面应按逻辑分辨率绘制，再按整数或 nearest-neighbor 规则缩放。
- HUD 不随摄像机滚动；关卡、玩家、敌人和收集物随摄像机滚动。

## Key Design Decisions (ADR)

### ADR-001: 原创 IP 边界

- Decision: 游戏角色、敌人、收集物、tile、关卡布局、名称、UI 表达和可选音频必须全部原创，不使用或临摹超级马里奥、任天堂或其他可识别商业 IP。
- Why: 这是用户明确约束，也是项目最重要的合规边界。
- Alternatives / Tradeoffs: 使用经典平台游戏素材、fan assets 或相似命名能降低制作成本，但会引入侵权和可识别 trade dress 风险，因此拒绝。使用授权第三方素材只有在许可、原创性和不可识别性可验证时才可作为后续扩展，不纳入 MVP 默认方案。

### ADR-002: 浏览器本地单页游戏

- Decision: MVP 设计为浏览器本地单页游戏，无服务端依赖、无账号、无联网数据。
- Why: 需求只确认浏览器可运行，单页本地架构足以满足可玩关卡、输入、计分、生命和胜负流程。
- Alternatives / Tradeoffs: 服务端排行榜或账号系统可扩展留存，但超出 MVP 且增加部署、隐私和测试复杂度。原生桌面或移动应用也不符合浏览器优先要求。

### ADR-003: Canvas 风格渲染契约

- Decision: MVP 使用画布式 2D 渲染契约，所有游戏对象按逻辑像素坐标绘制，并使用 nearest-neighbor 或整数缩放保持像素风格。
- Why: 横版平台跳跃需要稳定的摄像机、tile 渲染、碰撞可视化和像素缩放；画布式模型简单直接。
- Alternatives / Tradeoffs: DOM/CSS 实现便于普通 UI，但大量实体和摄像机滚动会更难保持确定性。WebGL/Three.js 性能更强，但对 2D MVP 复杂度过高。

### ADR-004: 键盘优先且支持 Arrow 与 WASD

- Decision: MVP 同时支持方向键和 WASD，跳跃支持 `ArrowUp`、`W`、`Space`，重开使用 `R`。
- Why: 用户明确要求键盘操作；同时支持两类常见布局能减少不必要的输入偏好阻塞。
- Alternatives / Tradeoffs: 只支持方向键或只支持 WASD 实现更少，但会降低可用性。可重绑定按键更灵活，但需要设置 UI 和持久化，不纳入 MVP。

### ADR-005: 直接进入可玩关卡

- Decision: MVP 打开后直接进入 `playing` 状态，不设计标题菜单；胜利和失败使用 overlay 提示并支持重开。
- Why: 核心验收关注可玩关卡、胜负和重开。直接进入关卡能更快验证完整游戏循环。
- Alternatives / Tradeoffs: 标题页更完整，但会增加状态和 UI 面，不是已确认需求。后续可以在不改变核心 gameplay 状态机的情况下增加 `menu` 状态。

### ADR-006: 单完整关卡优先

- Decision: MVP 只要求一个完整关卡，关卡内必须包含起点、平台、至少一种收集物、至少一种敌人、风险区域和终点。
- Why: 需求明确至少一个可玩关卡；一个完整关卡足以验证横版平台跳跃核心循环。
- Alternatives / Tradeoffs: 多关卡能提升内容量，但会增加关卡选择、进度和测试范围。无尽跑酷会改变“到达终点”的确认需求，因此不采用。

### ADR-007: 固定步长逻辑更新

- Decision: 游戏逻辑使用固定步长更新，渲染可按浏览器帧率执行。
- Why: 平台跳跃的碰撞、跳跃和 stomp 判定需要可预测行为，固定步长便于测试和调试。
- Alternatives / Tradeoffs: 完全可变 `dt` 实现简单，但在不同刷新率或掉帧情况下可能产生穿透和手感漂移。完整物理引擎能力强，但对 MVP 过重。

### ADR-008: Tile + AABB 碰撞

- Decision: 地形使用 tile grid 表达，玩家、敌人、收集物、危险区域和终点使用 AABB 碰撞。
- Why: 这是 2D 平台跳跃 MVP 的最小可控模型，便于实现 solid tile、落地、失败区域和目标触发。
- Alternatives / Tradeoffs: 像素级碰撞更精细但复杂。多边形碰撞适合斜坡和复杂地形，但 MVP 未要求这类关卡。

### ADR-009: 三条生命，损失生命回到起点

- Decision: MVP 初始生命为 3；损失生命后如果仍有剩余生命，玩家回到关卡起点，分数和当前 run 内已收集状态保留；生命归零进入失败。
- Why: 需求要求生命和失败状态，但未确认具体数值。3 条生命是简单、可测试、符合平台游戏直觉的 MVP 默认契约。
- Alternatives / Tradeoffs: 检查点能降低挫败感，但需要额外地图标记和状态。最后安全位置可能出现状态不确定。每次受伤仅短暂无敌不重置位置会增加关卡设计难度。

### ADR-010: MVP 不包含音频

- Decision: MVP 不设计音效或音乐契约。
- Why: 需求未确认音频，且明确核心是浏览器可玩、像素风格、键盘操作和玩法循环。
- Alternatives / Tradeoffs: 音频能增强反馈，但会带来资产原创性、浏览器自动播放限制和测试范围。后续可以添加原创音效，但必须遵守 ADR-001。

## Acceptance Criteria 映射

| 需求验收点 | 设计映射 | 可测试方式 |
| --- | --- | --- |
| 浏览器打开即可看到可玩游戏 | App Shell、Game Loop、Renderer、`bootstrapGame` | 在桌面浏览器加载入口，断言画布/HUD 可见且状态为 `playing` |
| 不出现商业 IP 内容 | ADR-001、Renderer 原创视觉边界、Level 原创数据 | 静态检查资产/命名；视觉审查关卡和实体 |
| 左移键移动角色 | Input、Physics、`moveLeft` 契约 | 模拟 `ArrowLeft`/`A`，断言玩家 x 坐标减少或被阻挡 |
| 右移键移动角色 | Input、Physics、`moveRight` 契约 | 模拟 `ArrowRight`/`D`，断言玩家 x 坐标增加或被阻挡 |
| 站在表面时可跳跃 | Jump 流程、`grounded` 不变量 | 设置玩家 grounded 后触发 jump，断言 y 速度向上 |
| 空中不能意外二段跳 | Jump 流程、ADR-008 | airborne 时触发 jump，断言不重置上升速度 |
| 关卡可到达终点并胜利 | Level System、GoalState、终点流程 | 将玩家移动到终点，断言状态进入 `win` |
| 胜利后普通玩法停止 | Game State Manager | `win` 状态下输入移动键，断言玩法状态不再推进 |
| 胜负后可重开 | Input、`restartRun` | `win`/`lose` 状态按 `R`，断言回到初始 `playing` |
| 收集物被移除 | Entity System、收集物流程 | 玩家碰撞收集物后断言 `collected = true` 且不再渲染 |
| 收集物加分 | Scoring | 碰撞收集物后断言 score 增加 100 |
| stomp 敌人加分 | Enemy 交互流程、Scoring | 从上方下落接触敌人，断言敌人失效且 score 增加 200 |
| 非 stomp 敌人接触损失生命 | Enemy 交互流程、Lives | 侧面接触敌人，断言 lives 减少 |
| 危险区域或跌落损失生命 | HazardState、生命损失流程 | 玩家进入 hazard/fall 区域，断言 lives 减少或进入 `lose` |
| 生命耗尽进入失败 | Scoring & Lives、状态机 | 设置 lives=1 后触发伤害，断言状态进入 `lose` |
| playing 状态显示分数和生命 | HUD / Overlay UI | 视觉或 DOM/canvas 辅助测试确认 HUD 文本存在 |
| 胜利状态清晰 | HUD / Overlay UI | 进入 `win` 后确认胜利 overlay 可见 |
| 失败状态清晰 | HUD / Overlay UI | 进入 `lose` 后确认失败 overlay 可见 |

## Spec 回填要求

本设计没有改变 `doc/proposal.md` 中的已确认关键行为，也没有修改既有 spec。

如果后续实现采用本设计中收敛的 MVP 默认契约，建议在进入实现前或实现完成后同步回填以下 spec，使需求源和实现行为一致：

- `doc/specs/2026-06-08-retro-pixel-platformer.md`：补充默认键位、初始 3 条生命、重开规则、损失生命回到起点、MVP 无音频、直接进入关卡。
- `doc/specs/index.md`：仅当 spec 状态从 `Requirements draft` 更新为更高确认状态时需要同步状态。

## 风险和测试策略

### 风险

- IP 相似性风险：即使素材是新画的，也可能因颜色、轮廓、敌人造型、关卡组合过于接近经典商业游戏而不可接受。
- 平台跳跃手感风险：重力、速度、跳跃高度和碰撞容差若未校准，会导致游戏虽然功能存在但难以游玩。
- 碰撞误判风险：stomp 与侧面伤害如果只基于重叠区域，容易出现误伤或误杀敌人。
- 浏览器帧率风险：可变帧率、后台恢复和低性能设备可能导致穿透、跳跃高度变化或摄像机抖动。
- 像素缩放风险：非整数缩放或默认图像平滑会破坏像素美术风格。
- 重开状态遗漏风险：如果重开没有从初始关卡数据重建状态，收集物、敌人、分数或生命可能残留。

### 测试策略

- 单元测试：
  - `Input`：按键映射、边沿触发、持续状态、销毁监听。
  - `Physics & Collision`：tile 阻挡、落地、头顶碰撞、边界限制、无二段跳。
  - `Enemy Interaction`：上方 stomp、侧面伤害、敌人失效后不再伤害。
  - `Scoring & Lives`：收集加分、stomp 加分、生命减少、生命归零失败。
  - `State Manager`：`playing`、`win`、`lose`、重开和初始状态恢复。
- 集成测试：
  - 加载关卡后从起点到终点的胜利路径。
  - 收集物、敌人、危险区域和终点在同一 run 内的组合行为。
  - `win` / `lose` 状态下普通玩法停止但重开有效。
- 浏览器验证：
  - 桌面浏览器打开入口后无需安装即可游玩。
  - HUD 分数和生命可见。
  - 像素画面边缘清晰，没有模糊缩放。
  - 摄像机跟随时不显示关卡外区域。
- 视觉/IP 审查：
  - 检查所有名称、角色、敌人、tile、收集物和终点是否原创。
  - 检查关卡布局是否避免复刻可识别商业 IP 关卡结构。
- 手测脚本：
  - 左右移动、跳跃、撞墙、落地。
  - 空中重复按跳跃键，确认无二段跳。
  - 收集物消失并加分。
  - 从上方踩敌人加分，侧面碰敌人掉生命。
  - 掉入失败区域扣生命，生命耗尽进入失败。
  - 到达终点进入胜利。
  - 胜利或失败后按 `R` 重开，确认分数、生命、实体和玩家位置恢复初始状态。
