# Retro Pixel Platformer Spec

## Status

Implemented MVP.

## Source

This spec summarizes the greenfield requirements captured in `doc/proposal.md` for an original browser-playable retro pixel platformer.

## Scope

The MVP is a browser-running, keyboard-controlled, original pixel-art side-scrolling platform game with at least one playable level. The player can run, jump, collect items, interact with enemies by avoidance or stomping, and reach a finish goal. The game includes score, lives, win state, lose state, and restart behavior.

## Confirmed Requirements

- Browser playable.
- Keyboard controlled.
- Original pixel-art style.
- At least one playable level.
- Includes running, jumping, collectibles, enemies, and finish goal.
- Includes score, lives, win state, and lose state.
- Excludes Super Mario, Nintendo, and recognizable commercial IP names, characters, assets, layouts, or trade dress.

## Non-Goals

- No implementation in the requirements phase.
- No technical architecture decision in the requirements phase.
- No commercial IP recreation.
- No requirement for multiple levels, online features, mobile touch controls, or audio in MVP unless later confirmed.

## Requirement Reference

Detailed user stories, EARS functional requirements, ADR candidates, acceptance criteria, constraints, and open questions are maintained in `doc/proposal.md`.

## Implemented MVP Defaults

The implementation in `index.html` and `src/game.js` uses the design-stage defaults from `doc/detailed-design.md`:

- Static browser app with no package manager, build step, server, account, network, audio, title menu, settings page, touch controls, or persistence.
- Direct-to-play single level named `Lantern Ridge`, with original programmatic pixel art and no external assets.
- Keyboard controls: `ArrowLeft` / `KeyA`, `ArrowRight` / `KeyD`, `ArrowUp` / `KeyW` / `Space`, and `KeyR` restart after win or lose.
- Fixed-step gameplay update, canvas rendering, nearest-neighbor scaling, tile collision, and AABB entity interactions.
- Initial lives: 3. Collectible score: 100. Stomp score: 200.
- Life loss respawns the player at the level start, keeps current run score and collected items, and grants short temporary invulnerability.
- Full restart after win or lose resets player, camera, score, lives, enemies, and collectibles.

Human originality/IP review remains a required final validation item for the level layout, visuals, and UI expression.
