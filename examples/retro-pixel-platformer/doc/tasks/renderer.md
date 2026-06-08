# Renderer

## 模块目标

实现原创像素风格的 2D 渲染契约，绘制关卡 tile、玩家、敌人、收集物、危险区、终点、HUD 基础文本和摄像机视图。画面必须使用逻辑像素坐标和 nearest-neighbor 或整数缩放保持像素边缘清晰。

## 依赖输入

- `doc/proposal.md`：EARS Runtime & Presentation；Acceptance Criteria / Browser Runtime、UI State。
- `doc/detailed-design.md`：模块 9 Renderer、Rendering 契约、原创视觉边界、ADR-001、ADR-003。
- 依赖契约：`GameState`、`LevelDefinition`、`RenderSurface`、`CameraState`。

## Out of Scope

- 不使用商业 IP 素材、名称、颜色组合、轮廓或标志性场景元素。
- 不实现音频、特效系统或复杂 sprite atlas pipeline。
- 不实现设置页或可换皮肤。

## 任务 Checklist

- [x] `AFK` 创建 canvas 或等价画布式 `RenderSurface`，包含 `clear`、`drawTile`、`drawSprite`、`drawText` 能力。Trace: Rendering Contract；ADR-003。
- [x] `AFK` 配置逻辑分辨率、CSS 尺寸和 image smoothing，保持 nearest-neighbor 像素缩放。Trace: EARS Runtime & Presentation；AC Browser Runtime。
- [x] `AFK` 实现摄像机偏移绘制，关卡和实体随摄像机滚动，HUD 不随摄像机滚动。Trace: Renderer Responsibilities；AC UI State。
- [x] `AFK` 绘制原创 tile、玩家、敌人、收集物、危险区和终点的最小像素外观。Trace: ADR-001；AC Browser Runtime。
- [x] `AFK` 避免使用管道、砖块、旗杆、蘑菇、乌龟等可识别商业 IP 组合。Trace: ADR-001；AC Browser Runtime。
- [x] `AFK` 实现 collected 收集物和 inactive 敌人不再渲染。Trace: Entity Data Invariants；AC Collectibles & Score、Enemies & Lives。
- [x] `AFK` 补充渲染冒烟测试或截图验证，确认画布非空、HUD 区域存在、像素平滑关闭。Trace: Testing Strategy / Browser Verification。
- [ ] `HITL` 执行最终视觉原创/IP 审查，确认角色、敌人、tile、终点和整体画面不构成可识别 trade dress。Trace: ADR-001；AC Browser Runtime。

## 验收标准

- 游戏画面在浏览器中非空可见。
- 像素边缘清晰，不因默认平滑导致模糊。
- 摄像机跟随玩家时不显示关卡边界外区域。
- 关卡、玩家、敌人、收集物、危险区、终点和 HUD 均可被识别。
- 视觉内容为原创，不出现可识别商业 IP。

## 测试要求

- 单元测试：RenderSurface 调用、摄像机坐标转换、隐藏 collected/inactive 实体。
- 浏览器验证：画布非空、HUD 可见、像素缩放清晰、摄像机不越界。
- 人工验收：视觉/IP 审查。

## AFK/HITL 标记

- `AFK`：渲染契约、程序化像素绘制和自动冒烟测试可独立完成。
- `HITL`：视觉原创/IP 审查必须人工确认。

## Blocked by

- 依赖 Level System 和 Entity System 提供稳定的实体和关卡数据。
- 依赖 HUD / Overlay UI 提供最终文案和状态展示要求。

## 可能修改的文件范围

- `src/rendering/*`
- `src/assets/*`
- `src/entities/*`
- `src/level/*`
- `src/styles/*`
- `tests/renderer.*`
