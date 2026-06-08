(function (global) {
  "use strict";

  var DEFAULT_CONFIG = Object.freeze({
    logicalWidth: 320,
    logicalHeight: 180,
    tileSize: 16,
    gravity: 900,
    maxFallSpeed: 360,
    playerMoveSpeed: 96,
    playerJumpSpeed: 285,
    stompBounceSpeed: 180,
    startingLives: 3,
    collectibleScore: 100,
    stompScore: 200,
    fixedStep: 1 / 60,
    maxFrameDelta: 0.08,
    maxStepsPerFrame: 5
  });

  var TILE = Object.freeze({
    EMPTY: 0,
    MOSS: 1,
    STONE: 2,
    LEDGE: 3
  });

  var KEY_MAP = Object.freeze({
    left: { ArrowLeft: true, KeyA: true },
    right: { ArrowRight: true, KeyD: true },
    jump: { ArrowUp: true, KeyW: true, Space: true },
    restart: { KeyR: true }
  });

  function cloneVector(vector) {
    return { x: vector.x, y: vector.y };
  }

  function mergeConfig(config) {
    var merged = {};
    Object.keys(DEFAULT_CONFIG).forEach(function (key) {
      merged[key] = DEFAULT_CONFIG[key];
    });
    Object.keys(config || {}).forEach(function (key) {
      if (Object.prototype.hasOwnProperty.call(DEFAULT_CONFIG, key)) {
        merged[key] = config[key];
      }
    });
    return merged;
  }

  function rectOf(entity) {
    if (entity.bounds) return entity.bounds;
    return {
      x: entity.position.x,
      y: entity.position.y,
      width: entity.size.x,
      height: entity.size.y
    };
  }

  function intersects(a, b) {
    return (
      a.x < b.x + b.width &&
      a.x + a.width > b.x &&
      a.y < b.y + b.height &&
      a.y + a.height > b.y
    );
  }

  function tileRect(tileX, tileY, tileSize) {
    return {
      x: tileX * tileSize,
      y: tileY * tileSize,
      width: tileSize,
      height: tileSize
    };
  }

  function createLevelRows() {
    var width = 86;
    var height = 12;
    var rows = [];
    for (var y = 0; y < height; y += 1) {
      var row = [];
      for (var x = 0; x < width; x += 1) row.push(TILE.EMPTY);
      rows.push(row);
    }

    function fill(y, x0, x1, tile) {
      for (var x = x0; x <= x1; x += 1) rows[y][x] = tile;
    }

    fill(10, 0, 17, TILE.MOSS);
    fill(10, 22, 35, TILE.MOSS);
    fill(10, 40, 54, TILE.MOSS);
    fill(10, 60, 85, TILE.MOSS);
    fill(11, 0, 85, TILE.STONE);
    fill(8, 8, 13, TILE.LEDGE);
    fill(7, 19, 25, TILE.LEDGE);
    fill(6, 31, 37, TILE.LEDGE);
    fill(8, 46, 52, TILE.LEDGE);
    fill(6, 58, 64, TILE.LEDGE);
    fill(7, 70, 75, TILE.LEDGE);
    fill(5, 78, 82, TILE.LEDGE);

    return rows;
  }

  var LEVELS = Object.freeze({
    "lantern-ridge": Object.freeze({
      id: "lantern-ridge",
      name: "Lantern Ridge",
      widthTiles: 86,
      heightTiles: 12,
      tileSize: 16,
      playerSpawn: Object.freeze({ x: 24, y: 128 }),
      solidTiles: createLevelRows(),
      enemies: Object.freeze([
        Object.freeze({
          id: "ember-mite-1",
          kind: "patroller",
          position: Object.freeze({ x: 178, y: 136 }),
          velocity: Object.freeze({ x: 34, y: 0 }),
          size: Object.freeze({ x: 14, y: 12 }),
          patrolMinX: 158,
          patrolMaxX: 242
        }),
        Object.freeze({
          id: "ember-mite-2",
          kind: "patroller",
          position: Object.freeze({ x: 680, y: 136 }),
          velocity: Object.freeze({ x: -38, y: 0 }),
          size: Object.freeze({ x: 14, y: 12 }),
          patrolMinX: 640,
          patrolMaxX: 778
        })
      ]),
      collectibles: Object.freeze([
        Object.freeze({ id: "glowseed-1", position: Object.freeze({ x: 98, y: 108 }), size: Object.freeze({ x: 8, y: 8 }), scoreValue: 100 }),
        Object.freeze({ id: "glowseed-2", position: Object.freeze({ x: 326, y: 80 }), size: Object.freeze({ x: 8, y: 8 }), scoreValue: 100 }),
        Object.freeze({ id: "glowseed-3", position: Object.freeze({ x: 494, y: 110 }), size: Object.freeze({ x: 8, y: 8 }), scoreValue: 100 }),
        Object.freeze({ id: "glowseed-4", position: Object.freeze({ x: 940, y: 78 }), size: Object.freeze({ x: 8, y: 8 }), scoreValue: 100 }),
        Object.freeze({ id: "glowseed-5", position: Object.freeze({ x: 1252, y: 60 }), size: Object.freeze({ x: 8, y: 8 }), scoreValue: 100 })
      ]),
      hazards: Object.freeze([
        Object.freeze({ id: "bramble-low-1", kind: "damage", bounds: Object.freeze({ x: 288, y: 154, width: 48, height: 6 }) }),
        Object.freeze({ id: "bramble-low-2", kind: "damage", bounds: Object.freeze({ x: 552, y: 154, width: 40, height: 6 }) }),
        Object.freeze({ id: "fall-field", kind: "fall", bounds: Object.freeze({ x: -64, y: 190, width: 1504, height: 64 }) })
      ]),
      goal: Object.freeze({ bounds: Object.freeze({ x: 1302, y: 48, width: 22, height: 32 }) })
    })
  });

  function loadLevel(id) {
    var level = LEVELS[id || "lantern-ridge"];
    if (!level) throw new Error("Unknown level: " + id);
    return level;
  }

  function cloneEnemy(enemy) {
    return {
      id: enemy.id,
      kind: enemy.kind,
      position: cloneVector(enemy.position),
      velocity: cloneVector(enemy.velocity),
      size: cloneVector(enemy.size),
      patrolMinX: enemy.patrolMinX,
      patrolMaxX: enemy.patrolMaxX,
      alive: true
    };
  }

  function cloneCollectible(collectible) {
    return {
      id: collectible.id,
      position: cloneVector(collectible.position),
      size: cloneVector(collectible.size),
      scoreValue: collectible.scoreValue,
      collected: false
    };
  }

  function cloneHazard(hazard) {
    return {
      id: hazard.id,
      kind: hazard.kind,
      bounds: {
        x: hazard.bounds.x,
        y: hazard.bounds.y,
        width: hazard.bounds.width,
        height: hazard.bounds.height
      }
    };
  }

  function createInitialGameState(level, config) {
    var mergedConfig = mergeConfig(config);
    return {
      status: "playing",
      score: 0,
      lives: mergedConfig.startingLives,
      levelId: level.id,
      player: {
        id: "player",
        position: cloneVector(level.playerSpawn),
        previousPosition: cloneVector(level.playerSpawn),
        velocity: { x: 0, y: 0 },
        size: { x: 12, y: 15 },
        spawnPoint: cloneVector(level.playerSpawn),
        facing: "right",
        grounded: false,
        invulnerableSeconds: 0
      },
      enemies: level.enemies.map(cloneEnemy),
      collectibles: level.collectibles.map(cloneCollectible),
      hazards: level.hazards.map(cloneHazard),
      goal: {
        bounds: {
          x: level.goal.bounds.x,
          y: level.goal.bounds.y,
          width: level.goal.bounds.width,
          height: level.goal.bounds.height
        }
      },
      camera: {
        position: { x: 0, y: 0 },
        viewport: { x: mergedConfig.logicalWidth, y: mergedConfig.logicalHeight }
      }
    };
  }

  function isSolidAt(level, tileX, tileY) {
    if (tileX < 0 || tileX >= level.widthTiles) return true;
    if (tileY < 0) return false;
    if (tileY >= level.heightTiles) return true;
    return level.solidTiles[tileY][tileX] !== TILE.EMPTY;
  }

  function querySolidTiles(level, bounds) {
    var tileSize = level.tileSize;
    var minX = Math.floor(bounds.x / tileSize);
    var maxX = Math.floor((bounds.x + bounds.width - 0.01) / tileSize);
    var minY = Math.floor(bounds.y / tileSize);
    var maxY = Math.floor((bounds.y + bounds.height - 0.01) / tileSize);
    var tiles = [];
    for (var y = minY; y <= maxY; y += 1) {
      for (var x = minX; x <= maxX; x += 1) {
        if (isSolidAt(level, x, y)) tiles.push(tileRect(x, y, tileSize));
      }
    }
    return tiles;
  }

  function createKeyboardInput(target) {
    var keysDown = {};
    var jumpPressed = false;
    var restartPressed = false;
    var destroyed = false;

    function codeIn(map, code) {
      return Object.prototype.hasOwnProperty.call(map, code);
    }

    function onKeyDown(event) {
      if (destroyed) return;
      var code = event.code || event.key;
      var wasDown = !!keysDown[code];
      keysDown[code] = true;
      if (!wasDown && codeIn(KEY_MAP.jump, code)) jumpPressed = true;
      if (!wasDown && codeIn(KEY_MAP.restart, code)) restartPressed = true;
      if (codeIn(KEY_MAP.left, code) || codeIn(KEY_MAP.right, code) || codeIn(KEY_MAP.jump, code) || codeIn(KEY_MAP.restart, code)) {
        if (event.preventDefault) event.preventDefault();
      }
    }

    function onKeyUp(event) {
      if (destroyed) return;
      var code = event.code || event.key;
      keysDown[code] = false;
    }

    target.addEventListener("keydown", onKeyDown);
    target.addEventListener("keyup", onKeyUp);

    return {
      read: function () {
        return {
          moveLeft: !!(keysDown.ArrowLeft || keysDown.KeyA),
          moveRight: !!(keysDown.ArrowRight || keysDown.KeyD),
          jumpDown: !!(keysDown.ArrowUp || keysDown.KeyW || keysDown.Space),
          jumpPressed: jumpPressed,
          restartPressed: restartPressed
        };
      },
      afterFrame: function () {
        jumpPressed = false;
        restartPressed = false;
      },
      destroy: function () {
        if (destroyed) return;
        destroyed = true;
        target.removeEventListener("keydown", onKeyDown);
        target.removeEventListener("keyup", onKeyUp);
      }
    };
  }

  function copyPlayer(player) {
    return {
      id: player.id,
      position: cloneVector(player.position),
      previousPosition: player.previousPosition ? cloneVector(player.previousPosition) : cloneVector(player.position),
      velocity: cloneVector(player.velocity),
      size: cloneVector(player.size),
      spawnPoint: cloneVector(player.spawnPoint),
      facing: player.facing,
      grounded: player.grounded,
      invulnerableSeconds: player.invulnerableSeconds
    };
  }

  function classifyEnemyContact(player, previousPlayer, enemy) {
    if (!enemy.alive) return "none";
    if (!intersects(rectOf(player), rectOf(enemy))) return "none";
    var previousBottom = previousPlayer.position.y + previousPlayer.size.y;
    var enemyTop = enemy.position.y;
    if (player.velocity.y >= 0 && previousBottom <= enemyTop + 4) return "stomp";
    return "damage";
  }

  function resolveActorVsTiles(actor, level, dt) {
    var result = {
      body: actor,
      hitLeft: false,
      hitRight: false,
      hitCeiling: false,
      hitGround: false
    };

    actor.position.x += actor.velocity.x * dt;
    var horizontalRect = rectOf(actor);
    querySolidTiles(level, horizontalRect).forEach(function (tile) {
      if (!intersects(rectOf(actor), tile)) return;
      if (actor.velocity.x > 0) {
        actor.position.x = tile.x - actor.size.x;
        result.hitRight = true;
      } else if (actor.velocity.x < 0) {
        actor.position.x = tile.x + tile.width;
        result.hitLeft = true;
      }
      actor.velocity.x = 0;
    });

    actor.grounded = false;
    actor.position.y += actor.velocity.y * dt;
    var verticalRect = rectOf(actor);
    querySolidTiles(level, verticalRect).forEach(function (tile) {
      if (!intersects(rectOf(actor), tile)) return;
      if (actor.velocity.y > 0) {
        actor.position.y = tile.y - actor.size.y;
        actor.grounded = true;
        result.hitGround = true;
      } else if (actor.velocity.y < 0) {
        actor.position.y = tile.y + tile.height;
        result.hitCeiling = true;
      }
      actor.velocity.y = 0;
    });

    return result;
  }

  function applyGravity(actor, dt, config) {
    actor.velocity.y = Math.min(config.maxFallSpeed, actor.velocity.y + config.gravity * dt);
  }

  function updateEnemy(enemy, level, dt, config) {
    if (!enemy.alive) return;
    applyGravity(enemy, dt, config);
    resolveActorVsTiles(enemy, level, dt);
    if (enemy.position.x <= enemy.patrolMinX) {
      enemy.position.x = enemy.patrolMinX;
      enemy.velocity.x = Math.abs(enemy.velocity.x || 30);
    } else if (enemy.position.x >= enemy.patrolMaxX) {
      enemy.position.x = enemy.patrolMaxX;
      enemy.velocity.x = -Math.abs(enemy.velocity.x || 30);
    }
  }

  function loseLife(state, level, config) {
    if (state.player.invulnerableSeconds > 0 || state.status !== "playing") return;
    state.lives = Math.max(0, state.lives - 1);
    if (state.lives <= 0) {
      state.status = "lose";
      state.player.velocity.x = 0;
      state.player.velocity.y = 0;
      return;
    }
    state.player.position = cloneVector(state.player.spawnPoint);
    state.player.previousPosition = cloneVector(state.player.spawnPoint);
    state.player.velocity = { x: 0, y: 0 };
    state.player.grounded = false;
    state.player.invulnerableSeconds = 1.2;
    updateCamera(state, level, config);
  }

  function updateCamera(state, level, config) {
    var maxX = level.widthTiles * level.tileSize - config.logicalWidth;
    var desiredX = state.player.position.x + state.player.size.x / 2 - config.logicalWidth * 0.42;
    state.camera.position.x = Math.max(0, Math.min(maxX, desiredX));
    state.camera.position.y = 0;
  }

  function updateGame(state, input, dt, level, config) {
    if (input.restartPressed && (state.status === "win" || state.status === "lose")) {
      return createInitialGameState(level, config);
    }
    if (state.status !== "playing") return state;

    var player = state.player;
    var previousPlayer = copyPlayer(player);
    player.previousPosition = cloneVector(player.position);
    player.invulnerableSeconds = Math.max(0, player.invulnerableSeconds - dt);

    var axis = 0;
    if (input.moveLeft) axis -= 1;
    if (input.moveRight) axis += 1;
    player.velocity.x = axis * config.playerMoveSpeed;
    if (axis < 0) player.facing = "left";
    if (axis > 0) player.facing = "right";
    if (input.jumpPressed && player.grounded) {
      player.velocity.y = -config.playerJumpSpeed;
      player.grounded = false;
    }

    applyGravity(player, dt, config);
    resolveActorVsTiles(player, level, dt);

    state.enemies.forEach(function (enemy) {
      updateEnemy(enemy, level, dt, config);
    });

    var playerRect = rectOf(player);
    state.collectibles.forEach(function (collectible) {
      if (!collectible.collected && intersects(playerRect, rectOf(collectible))) {
        collectible.collected = true;
        state.score += collectible.scoreValue || config.collectibleScore;
      }
    });

    state.enemies.forEach(function (enemy) {
      var contact = classifyEnemyContact(player, previousPlayer, enemy);
      if (contact === "stomp") {
        enemy.alive = false;
        player.velocity.y = -config.stompBounceSpeed;
        state.score += config.stompScore;
      } else if (contact === "damage") {
        loseLife(state, level, config);
      }
    });

    playerRect = rectOf(player);
    state.hazards.forEach(function (hazard) {
      if (state.status === "playing" && intersects(playerRect, hazard.bounds)) {
        loseLife(state, level, config);
      }
    });

    if (state.status === "playing" && intersects(rectOf(player), state.goal.bounds) && state.lives > 0) {
      state.status = "win";
      player.velocity.x = 0;
      player.velocity.y = 0;
    }

    updateCamera(state, level, config);
    return state;
  }

  function createCanvasSurface(canvas, config, level) {
    var ctx = canvas.getContext("2d");
    canvas.width = config.logicalWidth;
    canvas.height = config.logicalHeight;
    ctx.imageSmoothingEnabled = false;

    function drawText(text, x, y, color, size) {
      ctx.fillStyle = color || "#f6f1d8";
      ctx.font = (size || 8) + "px monospace";
      ctx.textBaseline = "top";
      ctx.fillText(text, Math.round(x), Math.round(y));
    }

    function drawPixelRect(x, y, width, height, color) {
      ctx.fillStyle = color;
      ctx.fillRect(Math.round(x), Math.round(y), Math.round(width), Math.round(height));
    }

    return {
      canvas: canvas,
      context: ctx,
      clear: function () {
        ctx.fillStyle = "#122335";
        ctx.fillRect(0, 0, config.logicalWidth, config.logicalHeight);
        drawPixelRect(0, 112, config.logicalWidth, 68, "#182d29");
        drawPixelRect(0, 0, config.logicalWidth, 38, "#1c3850");
        for (var i = 0; i < 13; i += 1) {
          var px = (i * 29 - Math.round(this.cameraX || 0) * 0.12) % 360;
          drawPixelRect(px, 28 + (i % 4) * 8, 14 + (i % 3) * 8, 2, "#2f5b68");
        }
      },
      drawTile: function (tileId, x, y) {
        if (tileId === TILE.EMPTY) return;
        var palette = tileId === TILE.MOSS
          ? ["#536c3d", "#8ca65d", "#273326"]
          : tileId === TILE.LEDGE
            ? ["#5b5750", "#b6a06f", "#2e3134"]
            : ["#363e42", "#637074", "#1e2527"];
        drawPixelRect(x, y, 16, 16, palette[0]);
        drawPixelRect(x, y, 16, 3, palette[1]);
        drawPixelRect(x + 1, y + 12, 14, 3, palette[2]);
        drawPixelRect(x + 3, y + 5, 3, 3, palette[2]);
        drawPixelRect(x + 10, y + 7, 4, 2, palette[1]);
      },
      drawSprite: function (spriteId, x, y, flipX, pulse) {
        if (spriteId === "player") {
          drawPixelRect(x + 3, y + 2, 6, 3, "#f2d179");
          drawPixelRect(x + 2, y + 5, 8, 6, "#3aa094");
          drawPixelRect(x + 4, y + 1, 5, 2, "#fff3a8");
          drawPixelRect(x + (flipX ? 2 : 8), y + 6, 2, 2, "#18201d");
          drawPixelRect(x + 1, y + 11, 4, 4, "#28384c");
          drawPixelRect(x + 7, y + 11, 4, 4, "#28384c");
          if (pulse) drawPixelRect(x, y, 12, 1, "#f6f1d8");
        } else if (spriteId === "enemy") {
          drawPixelRect(x + 1, y + 4, 12, 7, "#b24c3f");
          drawPixelRect(x + 3, y + 2, 8, 3, "#ec8d57");
          drawPixelRect(x + 3, y + 6, 2, 2, "#1b1715");
          drawPixelRect(x + 9, y + 6, 2, 2, "#1b1715");
          drawPixelRect(x + 1, y + 11, 3, 1, "#f2c078");
          drawPixelRect(x + 10, y + 11, 3, 1, "#f2c078");
        } else if (spriteId === "collectible") {
          drawPixelRect(x + 2, y, 4, 2, "#f6f1d8");
          drawPixelRect(x + 1, y + 2, 6, 4, "#f0c85a");
          drawPixelRect(x + 3, y + 3, 2, 2, "#fff4a6");
          drawPixelRect(x + 2, y + 6, 4, 2, "#8fae4a");
        } else if (spriteId === "goal") {
          drawPixelRect(x + 8, y, 4, 32, "#d9c38a");
          drawPixelRect(x, y + 3, 16, 5, "#78c2ad");
          drawPixelRect(x + 2, y + 10, 13, 4, "#f0c85a");
          drawPixelRect(x + 4, y + 17, 10, 3, "#d45f45");
        }
      },
      drawText: drawText,
      drawPixelRect: drawPixelRect
    };
  }

  function renderGame(state, surface, level, config) {
    var ctx = surface.context;
    var cameraX = Math.round(state.camera.position.x);
    surface.cameraX = cameraX;
    surface.clear();

    var startTileX = Math.max(0, Math.floor(cameraX / level.tileSize) - 1);
    var endTileX = Math.min(level.widthTiles - 1, Math.ceil((cameraX + config.logicalWidth) / level.tileSize) + 1);
    for (var y = 0; y < level.heightTiles; y += 1) {
      for (var x = startTileX; x <= endTileX; x += 1) {
        surface.drawTile(level.solidTiles[y][x], x * level.tileSize - cameraX, y * level.tileSize);
      }
    }

    state.hazards.forEach(function (hazard) {
      if (hazard.kind !== "damage") return;
      surface.drawPixelRect(hazard.bounds.x - cameraX, hazard.bounds.y, hazard.bounds.width, hazard.bounds.height, "#c8553d");
      surface.drawPixelRect(hazard.bounds.x - cameraX, hazard.bounds.y - 3, hazard.bounds.width, 3, "#f0a25e");
    });

    surface.drawSprite("goal", state.goal.bounds.x - cameraX, state.goal.bounds.y, false);

    state.collectibles.forEach(function (collectible) {
      if (!collectible.collected) {
        surface.drawSprite("collectible", collectible.position.x - cameraX, collectible.position.y, false);
      }
    });

    state.enemies.forEach(function (enemy) {
      if (enemy.alive) {
        surface.drawSprite("enemy", enemy.position.x - cameraX, enemy.position.y, enemy.velocity.x < 0);
      }
    });

    var invulnPulse = state.player.invulnerableSeconds > 0 && Math.floor(state.player.invulnerableSeconds * 12) % 2 === 0;
    surface.drawSprite(
      "player",
      state.player.position.x - cameraX,
      state.player.position.y,
      state.player.facing === "left",
      invulnPulse
    );

    surface.drawPixelRect(0, 0, config.logicalWidth, 18, "rgba(10, 16, 18, 0.82)");
    surface.drawText("SCORE " + String(state.score).padStart(4, "0"), 8, 5, "#f6f1d8", 8);
    surface.drawText("LIVES " + state.lives, 118, 5, "#f6f1d8", 8);
    surface.drawText(level.name, 224, 5, "#b6c690", 8);

    if (state.status === "win" || state.status === "lose") {
      ctx.fillStyle = "rgba(9, 13, 14, 0.78)";
      ctx.fillRect(0, 0, config.logicalWidth, config.logicalHeight);
      var title = state.status === "win" ? "RIDGE CLEARED" : "RUN ENDED";
      var subtitle = state.status === "win" ? "The lantern path is bright." : "Press R for a fresh run.";
      surface.drawPixelRect(70, 54, 180, 64, "#202924");
      surface.drawPixelRect(70, 54, 180, 4, "#b8ca75");
      surface.drawText(title, 98, 68, "#f6f1d8", 12);
      surface.drawText(subtitle, 86, 88, "#cbd9ae", 8);
      surface.drawText("R RESTART", 128, 102, "#f0c85a", 8);
    }
  }

  function createGameLoop(options) {
    var stateRef = options.stateRef;
    var input = options.input;
    var level = options.level;
    var config = options.config;
    var surface = options.surface;
    var raf = options.raf || global.requestAnimationFrame.bind(global);
    var caf = options.caf || global.cancelAnimationFrame.bind(global);
    var frameId = null;
    var lastTime = 0;
    var accumulator = 0;
    var running = false;

    function frame(timeMs) {
      if (!running) return;
      if (!lastTime) lastTime = timeMs;
      var frameDelta = Math.min(config.maxFrameDelta, (timeMs - lastTime) / 1000);
      lastTime = timeMs;
      accumulator += frameDelta;
      var steps = 0;
      var inputState = input.read();
      while (accumulator >= config.fixedStep && steps < config.maxStepsPerFrame) {
        stateRef.current = updateGame(stateRef.current, inputState, config.fixedStep, level, config);
        accumulator -= config.fixedStep;
        steps += 1;
      }
      if (steps >= config.maxStepsPerFrame) accumulator = 0;
      renderGame(stateRef.current, surface, level, config);
      input.afterFrame();
      frameId = raf(frame);
    }

    return {
      start: function () {
        if (running) return;
        running = true;
        frameId = raf(frame);
      },
      stop: function () {
        running = false;
        if (frameId !== null) caf(frameId);
        frameId = null;
      },
      isRunning: function () {
        return running;
      }
    };
  }

  function bootstrapGame(root, config) {
    if (!root) throw new Error("bootstrapGame requires a root element");
    var mergedConfig = mergeConfig(config);
    var level = loadLevel("lantern-ridge");
    var stateRef = { current: createInitialGameState(level, mergedConfig) };

    root.innerHTML = "";
    var shell = document.createElement("section");
    shell.className = "game-shell";
    var frame = document.createElement("div");
    frame.className = "game-frame";
    var canvas = document.createElement("canvas");
    canvas.className = "game-canvas";
    canvas.setAttribute("aria-label", "Lantern Ridge Run playfield");
    canvas.setAttribute("role", "img");
    var hint = document.createElement("p");
    hint.className = "game-hint";
    hint.textContent = "Move with Arrow keys or A/D. Jump with ArrowUp, W, or Space. Press R after victory or defeat.";
    frame.appendChild(canvas);
    shell.appendChild(frame);
    shell.appendChild(hint);
    root.appendChild(shell);

    var input = createKeyboardInput(global);
    var surface = createCanvasSurface(canvas, mergedConfig, level);
    var loop = createGameLoop({
      stateRef: stateRef,
      input: input,
      level: level,
      config: mergedConfig,
      surface: surface
    });

    var controller = {
      startRun: function () {
        if (stateRef.current.status === "booting") {
          stateRef.current = createInitialGameState(level, mergedConfig);
        }
        loop.start();
      },
      restartRun: function () {
        stateRef.current = createInitialGameState(level, mergedConfig);
        renderGame(stateRef.current, surface, level, mergedConfig);
      },
      destroy: function () {
        loop.stop();
        input.destroy();
        root.innerHTML = "";
      },
      getState: function () {
        return stateRef.current;
      },
      step: function (inputState, dt) {
        stateRef.current = updateGame(stateRef.current, inputState || {}, dt || mergedConfig.fixedStep, level, mergedConfig);
        renderGame(stateRef.current, surface, level, mergedConfig);
        return stateRef.current;
      }
    };

    renderGame(stateRef.current, surface, level, mergedConfig);
    loop.start();
    return controller;
  }

  global.RetroPixelPlatformer = {
    DEFAULT_CONFIG: DEFAULT_CONFIG,
    TILE: TILE,
    bootstrapGame: bootstrapGame,
    createKeyboardInput: createKeyboardInput,
    updateGame: updateGame,
    loadLevel: loadLevel,
    createInitialGameState: createInitialGameState,
    isSolidAt: isSolidAt,
    querySolidTiles: querySolidTiles,
    intersects: intersects,
    classifyEnemyContact: classifyEnemyContact,
    resolveActorVsTiles: resolveActorVsTiles,
    createCanvasSurface: createCanvasSurface,
    renderGame: renderGame,
    createGameLoop: createGameLoop
  };
})(window);
