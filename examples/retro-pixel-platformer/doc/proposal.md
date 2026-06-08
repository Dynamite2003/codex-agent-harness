# Retro Pixel Platformer Proposal

## Context

本阶段是需求阶段，只生成可审阅、可确认、可进入设计阶段的 Spec-first artifact，不进行设计、任务拆分或代码实现。

当前项目目录为 `/Users/bytedance/Documents/Programs/Vibe2Spec/examples/retro-pixel-platformer`。目录内未发现现有应用源码、README、包管理配置或上游产品文档，仅存在 `.harness` 元数据。因此本需求按 greenfield 浏览器游戏项目处理，不依赖现有运行系统。

### 目标

创作一款原创复古像素横版平台跳跃游戏。玩家控制原创角色在至少一个可玩关卡中奔跑、跳跃、收集物品、躲避或踩踏敌人，并到达终点。游戏必须浏览器可运行，提供键盘操作、像素美术风格、计分、生命、胜负状态，并避免使用超级马里奥、任天堂角色、名称、素材、关卡布局或任何可识别商业 IP。

### 输入

- 用户明确需求：原创复古像素横版平台跳跃游戏。
- 阶段约束：只完成需求阶段，输出规划 artifacts，不开始编码。
- 上游 artifact：无。
- 项目现状：未发现现有源码，按新项目需求整理。

### 输出

- `doc/proposal.md`：本需求文档。
- `doc/specs/index.md`：独立 spec 索引。
- `doc/specs/2026-06-08-retro-pixel-platformer.md`：本 feature 的独立需求 spec。

### 步骤

1. 阅读项目目录和必要文件，确认是否依赖现有系统。
2. 区分用户已确认事实、建议假设和待确认问题。
3. 使用 EARS 写出原子化功能需求。
4. 使用 ADR Candidates 记录关键决策的原因、替代方案和权衡。
5. 使用 GIVEN-WHEN-THEN 写出可手测或自动化验证的验收标准。
6. 列出开放问题，供进入设计阶段前确认。

### Confirmed Facts

- 游戏必须是原创内容，不能使用超级马里奥、任天堂或其他可识别商业 IP 的角色、名称、素材或关卡布局。
- 游戏必须能在浏览器中运行。
- 游戏必须采用像素美术风格。
- 游戏必须使用键盘操作。
- 游戏必须至少包含一个可玩关卡。
- 核心玩法必须包含奔跑、跳跃、收集物品、躲避或踩踏敌人、到达终点。
- 游戏必须包含计分、生命、胜利状态和失败状态。
- 当前阶段只产出需求文档和 spec artifacts，不进行实际编码。

### Suggested Assumptions

以下内容是可进入设计阶段时考虑的建议，不是已确认事实：

- 建议优先实现单人离线浏览器游戏。
- 建议优先支持桌面键盘，因为用户明确要求键盘操作。
- 建议将第一关设计为短关卡，用于验证完整游戏循环，而不是追求大量内容。
- 建议像素美术可使用程序化绘制、CSS/canvas 绘制或原创像素图块，但具体技术方案留到设计阶段决策。

### Independent Spec Decision

本需求属于新 feature 且会形成完整浏览器游戏应用，包含游戏循环、输入、物理、关卡、实体状态、计分/生命和胜负流程，具有跨模块产品行为。因此需要独立 spec。已创建：

- `doc/specs/index.md`
- `doc/specs/2026-06-08-retro-pixel-platformer.md`

## Goals & Non-Goals

### Goals

- 定义一款原创复古像素横版平台跳跃游戏的 MVP 需求边界。
- 明确核心玩家体验：移动、跳跃、收集、敌人交互、终点通关。
- 明确必须具备的运行环境、输入方式、状态反馈和可验收行为。
- 明确 IP 合规边界，避免可识别商业 IP 复刻。
- 为后续设计阶段提供足够清晰的需求依据。

### Non-Goals

- 本阶段不选择具体技术栈、渲染引擎或项目架构。
- 本阶段不设计具体关卡布局、物理参数、角色外观或敌人造型。
- 本阶段不拆分开发任务。
- 本阶段不编写、生成或修改游戏运行代码。
- MVP 不要求多人模式、联网排行榜、移动端触控、关卡编辑器或长期存档。

## User Stories

- 作为玩家，我想用键盘控制原创角色左右移动和跳跃，以便完成横版平台关卡。
- 作为玩家，我想收集关卡内的物品并看到分数变化，以便获得明确的即时反馈。
- 作为玩家，我想通过躲避或踩踏敌人处理威胁，以便体验平台跳跃游戏的风险与技巧。
- 作为玩家，我想看到生命数量，以便理解自己还能承受多少失误。
- 作为玩家，我想到达关卡终点并看到胜利状态，以便确认自己完成了关卡。
- 作为玩家，我想在生命耗尽后看到失败状态，并能重新开始，以便继续尝试。
- 作为项目维护者，我想需求明确禁止商业 IP 复刻，以便后续设计和实现保持原创。

## Functional Requirements (EARS)

### Runtime & Presentation

- WHEN the player opens the game in a supported desktop browser THE SYSTEM SHALL present a playable game screen without requiring native installation.
- THE SYSTEM SHALL use an original retro pixel-art visual style for the player character, enemies, collectibles, tiles, and level presentation.
- THE SYSTEM SHALL NOT use Super Mario, Nintendo, or any recognizable commercial IP names, characters, sprites, audio, level layouts, logos, or trade dress.
- THE SYSTEM SHALL provide visible score, lives, and game state feedback during play.

### Input

- WHEN the player presses the configured left movement key THE SYSTEM SHALL move the player character left, subject to collision and level boundaries.
- WHEN the player presses the configured right movement key THE SYSTEM SHALL move the player character right, subject to collision and level boundaries.
- WHEN the player presses the configured jump key while the character is grounded THE SYSTEM SHALL make the character jump.
- WHEN the player presses the jump key while the character is not eligible to jump THE SYSTEM SHALL prevent unintended extra jumps unless a later confirmed design explicitly permits them.
- WHEN the game is in win or lose state and the player triggers restart THE SYSTEM SHALL restart the playable level from its initial state.

### Level & Movement

- THE SYSTEM SHALL include at least one playable side-scrolling platform level with a start area, traversable platforms, collectible items, enemies, hazards or risk areas, and a finish goal.
- WHEN the player character intersects solid level geometry THE SYSTEM SHALL prevent movement through that geometry.
- WHEN gravity applies to the player character THE SYSTEM SHALL pull the character downward until blocked by a valid surface or until a failure condition is reached.
- WHEN the player reaches the finish goal while still alive THE SYSTEM SHALL enter a win state.

### Collectibles & Scoring

- WHEN the player character collects a collectible THE SYSTEM SHALL remove that collectible from the current level state.
- WHEN the player character collects a collectible THE SYSTEM SHALL increase the score by a visible amount.
- WHEN the player defeats an enemy by a valid stomp interaction THE SYSTEM SHALL increase the score by a visible amount.
- THE SYSTEM SHALL preserve score during the current run until restart or game reset.

### Enemies, Damage, Lives

- THE SYSTEM SHALL include at least one original enemy type with a predictable movement or threat pattern.
- WHEN the player character lands on an enemy from above under valid stomp conditions THE SYSTEM SHALL defeat or neutralize that enemy.
- WHEN the player character contacts an enemy from a non-stomp direction THE SYSTEM SHALL apply damage or life loss.
- WHEN the player character hits a damaging hazard or falls into a failure area THE SYSTEM SHALL apply damage or life loss.
- WHEN the player loses a life but still has remaining lives THE SYSTEM SHALL respawn the character or reset the current attempt according to the later confirmed design.
- WHEN the player has no lives remaining THE SYSTEM SHALL enter a lose state.

### Game States

- THE SYSTEM SHALL support at minimum playing, win, lose, and restartable states.
- WHEN the game enters win state THE SYSTEM SHALL stop normal gameplay progression and show a clear victory indication.
- WHEN the game enters lose state THE SYSTEM SHALL stop normal gameplay progression and show a clear failure indication.
- WHEN the game restarts THE SYSTEM SHALL reset player position, level entities, score, lives, and game state according to MVP rules confirmed during design.

## Key Decisions / ADR Candidates

### ADR-001: Original IP Boundary

- Decision: The game will use fully original characters, enemies, collectibles, tiles, names, audio, and level layouts.
- Why: The user explicitly requires avoiding Super Mario, Nintendo characters, names, assets, layouts, and recognizable commercial IP.
- Alternatives: Recreate classic platformer elements more closely; use public fan assets; use commercial-inspired naming. These alternatives are rejected because they increase IP and recognizability risk.

### ADR-002: Browser-Playable MVP

- Decision: The MVP will target browser runtime.
- Why: Browser playability is a confirmed requirement and keeps the game accessible without native installation.
- Alternatives: Native desktop build, mobile app, or engine-specific packaged export. These may be future options but are outside the confirmed MVP.

### ADR-003: Keyboard-First Controls

- Decision: The MVP will define keyboard controls as the required input method.
- Why: The user explicitly requires keyboard operation.
- Alternatives: Touch controls, gamepad controls, mouse controls. These can be optional future enhancements but are not required for MVP acceptance.

### ADR-004: One Complete Level Before Content Expansion

- Decision: The MVP will require at least one complete playable level with start, obstacles, collectibles, enemies, and finish.
- Why: The user requires at least one playable level and complete win/lose flow. One complete level is enough to validate the game loop before adding content volume.
- Alternatives: Multiple shallow levels; endless runner format; sandbox demo. These alternatives are not required and may dilute MVP focus.

### ADR-005: Pixel Art Style Without Commercial Asset Reuse

- Decision: The visual direction will be retro pixel art using original assets or original programmatic rendering.
- Why: Pixel style is required, but commercial IP assets are prohibited.
- Alternatives: Use downloaded sprite packs, imitate recognizable classic sprites, or use vector/modern art. Downloaded packs may be acceptable only if license and originality are verified later; recognizable imitation is rejected.

## Acceptance Criteria (GIVEN-WHEN-THEN)

### Browser Runtime

- GIVEN a supported desktop browser WHEN the user opens the game entry point THEN the game screen is visible and playable without native installation.
- GIVEN the game is loaded WHEN the user inspects the visible game content THEN no Super Mario, Nintendo, or recognizable commercial IP names, characters, sprites, logos, or layouts are present.

### Controls

- GIVEN the game is in playing state WHEN the user presses the left movement key THEN the player character moves left unless blocked by terrain or boundary.
- GIVEN the game is in playing state WHEN the user presses the right movement key THEN the player character moves right unless blocked by terrain or boundary.
- GIVEN the player character is standing on a valid surface WHEN the user presses the jump key THEN the character jumps upward.
- GIVEN the player character is airborne and no air-jump mechanic has been confirmed WHEN the user presses the jump key THEN the character does not perform an unintended extra jump.

### Level Completion

- GIVEN the player starts the playable level WHEN the player traverses platforms and reaches the finish goal alive THEN the game enters win state.
- GIVEN the game has entered win state WHEN normal movement keys are pressed THEN normal gameplay progression is stopped or clearly completed.
- GIVEN the game has entered win or lose state WHEN the user triggers restart THEN a fresh playable run starts.

### Collectibles & Score

- GIVEN a collectible is present in the level WHEN the player character touches it THEN the collectible disappears from the active level.
- GIVEN the player collects an item WHEN the score display updates THEN the score is higher than before collection.
- GIVEN the player defeats an enemy through valid stomp interaction WHEN the score display updates THEN the score is higher than before the enemy was defeated.

### Enemies & Lives

- GIVEN an enemy is active in the level WHEN the player lands on it from above under valid stomp conditions THEN the enemy is defeated or neutralized.
- GIVEN an enemy is active in the level WHEN the player contacts it from a non-stomp direction THEN the player loses health or one life.
- GIVEN the player falls into a failure area or contacts a damaging hazard WHEN the damage is applied THEN the life count decreases or the game reaches lose state if no lives remain.
- GIVEN the player has no lives remaining WHEN another life-loss condition occurs THEN the game enters lose state.

### UI State

- GIVEN the game is in playing state WHEN the user views the screen THEN score and lives are visible.
- GIVEN the player wins WHEN the win state appears THEN the game communicates victory clearly.
- GIVEN the player loses WHEN the lose state appears THEN the game communicates failure clearly.

## Out of Scope

- Actual code implementation.
- Detailed architecture, rendering engine choice, asset pipeline, or module decomposition.
- Detailed level map layout and final art direction.
- Multiple levels beyond the required first playable level.
- Online features, accounts, cloud saves, leaderboards, achievements, monetization, analytics, ads, or social sharing.
- Mobile touch controls and gamepad support unless later confirmed.
- Audio requirements unless later confirmed.
- Accessibility requirements beyond visible state feedback unless later confirmed.

## Constraints

- Only current-stage artifacts may be modified.
- No code generation or implementation in this phase.
- Requirements must be reviewable before entering design.
- Critical decisions that are not confirmed must remain open questions or design-stage decisions.
- The game must be original and avoid recognizable commercial IP.
- The game must run in a browser.
- The game must support keyboard operation.
- The MVP must include at least one playable level with score, lives, and win/lose states.

## Open Questions

These questions should be answered before or during the next design stage. They do not block this requirements artifact because the MVP boundary above remains valid without choosing their final answers.

1. Which keyboard layout should be primary: Arrow keys, WASD, or both?
2. Should the MVP include audio effects/music, or stay silent for the first playable version?
3. Should the player have a fixed number of lives such as 3, or should the design stage choose the exact value?
4. Should damage respawn the player at the level start, at a checkpoint, or at the last safe position?
5. Should the first release target only desktop browsers, or include responsive scaling for smaller screens while still requiring keyboard input?
6. Are there accessibility requirements such as pause, reduced motion, remappable keys, color contrast targets, or screen-reader labels for menus?
7. Should the game include a title/menu screen, or can it start directly in the playable level for MVP?
