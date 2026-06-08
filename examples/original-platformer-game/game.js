(function () {
  "use strict";

  const canvas = document.getElementById("game");
  const ctx = canvas.getContext("2d");
  const scoreEl = document.getElementById("score");
  const coinsEl = document.getElementById("coins");
  const livesEl = document.getElementById("lives");
  const timeEl = document.getElementById("time");
  const overlay = document.getElementById("overlay");
  const startButton = document.getElementById("start");

  const W = canvas.width;
  const H = canvas.height;
  const TILE = 32;
  const WORLD_W = 5760;
  const GRAVITY = 0.62;
  const MAX_FALL = 16;
  const GROUND_Y = 464;

  const keys = new Set();
  const touch = { left: false, right: false, jump: false };
  let audio;
  let lastTime = 0;
  let running = false;
  let paused = false;
  let gameOver = false;
  let won = false;
  let timer = 300;
  let timeBank = 0;
  let score = 0;
  let coins = 0;
  let lives = 3;
  let camera = 0;
  let particles = [];
  let floatingText = [];
  let platforms = [];
  let blocks = [];
  let coinItems = [];
  let enemies = [];
  let hazards = [];
  let flag = { x: WORLD_W - 360, y: GROUND_Y - 224, w: 24, h: 224 };
  let player;

  const palettes = {
    grass: ["#49aa4b", "#2f7e3d", "#23633a"],
    earth: ["#9a6238", "#6d432b", "#503124"],
    brick: ["#c96b3c", "#8f3927", "#f3a35b"],
    crate: ["#f2b94c", "#98642a", "#fff0a7"],
    hero: ["#e34e45", "#2454a6", "#ffe0b8", "#3b2b2b", "#2fc3b3"],
    enemy: ["#7c4cb2", "#3b2665", "#f5d36a"],
  };

  function rect(x, y, w, h) {
    return { x, y, w, h };
  }

  function intersects(a, b) {
    return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
  }

  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function makeAudio() {
    if (audio) return audio;
    const Ctor = window.AudioContext || window.webkitAudioContext;
    if (!Ctor) return null;
    audio = new Ctor();
    return audio;
  }

  function beep(freq, duration, type, volume) {
    const ac = makeAudio();
    if (!ac) return;
    const osc = ac.createOscillator();
    const gain = ac.createGain();
    osc.type = type || "square";
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(volume || 0.06, ac.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + duration);
    osc.connect(gain).connect(ac.destination);
    osc.start();
    osc.stop(ac.currentTime + duration);
  }

  function buildLevel() {
    platforms = [];
    blocks = [];
    coinItems = [];
    enemies = [];
    hazards = [];
    particles = [];
    floatingText = [];

    const gaps = [
      [832, 928],
      [1536, 1664],
      [2464, 2624],
      [3500, 3628],
      [4544, 4640],
    ];

    let x = 0;
    while (x < WORLD_W) {
      const gap = gaps.find(([a, b]) => x >= a && x < b);
      if (!gap) {
        platforms.push(rect(x, GROUND_Y, TILE, H - GROUND_Y));
      }
      x += TILE;
    }

    addPlatform(448, 368, 5);
    addPlatform(1056, 336, 4);
    addPlatform(1224, 288, 3);
    addPlatform(1864, 368, 6);
    addPlatform(2208, 304, 4);
    addPlatform(2784, 368, 4);
    addPlatform(3104, 320, 5);
    addPlatform(3868, 352, 5);
    addPlatform(4224, 288, 4);
    addPlatform(4864, 352, 5);
    addPlatform(5200, 304, 5);

    addBlock(576, 304, "coin");
    addBlock(640, 304, "gem");
    addBlock(704, 304, "coin");
    addBlock(1168, 240, "coin");
    addBlock(1264, 240, "spring");
    addBlock(1952, 272, "coin");
    addBlock(2048, 272, "gem");
    addBlock(2880, 272, "coin");
    addBlock(3152, 256, "spring");
    addBlock(3968, 288, "coin");
    addBlock(4288, 224, "gem");
    addBlock(5120, 256, "coin");

    addCoinArc(240, 362, 6);
    addCoinArc(1008, 266, 5);
    addCoinArc(1736, 358, 8);
    addCoinArc(2656, 346, 7);
    addCoinArc(3728, 326, 7);
    addCoinArc(4736, 348, 5);

    addEnemy(736, GROUND_Y - 30, 650, 810);
    addEnemy(1376, GROUND_Y - 30, 1300, 1510);
    addEnemy(2096, 338, 1880, 2180);
    addEnemy(3008, GROUND_Y - 30, 2768, 3230);
    addEnemy(4128, GROUND_Y - 30, 3760, 4420);
    addEnemy(5088, 322, 4880, 5320);

    hazards.push(rect(2528, GROUND_Y - 18, 88, 18));
    hazards.push(rect(3544, GROUND_Y - 18, 74, 18));
    hazards.push(rect(4576, GROUND_Y - 18, 64, 18));
  }

  function addPlatform(x, y, count) {
    for (let i = 0; i < count; i += 1) platforms.push(rect(x + i * TILE, y, TILE, TILE));
  }

  function addBlock(x, y, type) {
    blocks.push({ x, y, w: TILE, h: TILE, type, used: false, bump: 0 });
  }

  function addCoinArc(x, y, count) {
    for (let i = 0; i < count; i += 1) {
      const lift = Math.sin((i / Math.max(1, count - 1)) * Math.PI) * 42;
      coinItems.push({ x: x + i * 42, y: y - lift, w: 18, h: 18, taken: false, spin: i * 0.7 });
    }
  }

  function addEnemy(x, y, minX, maxX) {
    enemies.push({ x, y, w: 30, h: 30, vx: -1.15, vy: 0, minX, maxX, alive: true, squash: 0 });
  }

  function resetPlayer() {
    player = {
      x: 84,
      y: GROUND_Y - 58,
      w: 30,
      h: 48,
      vx: 0,
      vy: 0,
      facing: 1,
      grounded: false,
      invuln: 0,
      jumpHold: 0,
      spawnX: 84,
      spawnY: GROUND_Y - 58,
    };
  }

  function resetGame() {
    score = 0;
    coins = 0;
    lives = 3;
    timer = 300;
    timeBank = 0;
    camera = 0;
    gameOver = false;
    won = false;
    paused = false;
    buildLevel();
    resetPlayer();
    updateHud();
  }

  function startGame() {
    if (audio && audio.state === "suspended") audio.resume();
    resetGame();
    running = true;
    overlay.classList.add("hidden");
    lastTime = performance.now();
    requestAnimationFrame(loop);
  }

  function updateHud() {
    scoreEl.textContent = String(score).padStart(6, "0");
    coinsEl.textContent = "x" + String(coins).padStart(2, "0");
    livesEl.textContent = String(lives);
    timeEl.textContent = String(Math.max(0, Math.ceil(timer))).padStart(3, "0");
  }

  function readInput() {
    const left = keys.has("ArrowLeft") || keys.has("KeyA") || touch.left;
    const right = keys.has("ArrowRight") || keys.has("KeyD") || touch.right;
    const jump = keys.has("Space") || keys.has("ArrowUp") || keys.has("KeyW") || touch.jump;
    const dash = keys.has("ShiftLeft") || keys.has("ShiftRight");
    return { left, right, jump, dash };
  }

  function loop(now) {
    if (!running) return;
    const dt = Math.min(2, (now - lastTime) / 16.67);
    lastTime = now;
    if (!paused && !gameOver && !won) update(dt);
    draw();
    requestAnimationFrame(loop);
  }

  function update(dt) {
    const input = readInput();
    updatePlayer(input, dt);
    updateEnemies(dt);
    updateItems(dt);
    updateParticles(dt);
    camera = clamp(player.x - 290, 0, WORLD_W - W);
    timeBank += dt;
    if (timeBank >= 60) {
      timeBank -= 60;
      timer -= 1;
      if (timer <= 0) hurtPlayer(true);
      updateHud();
    }
    if (player.y > H + 120) hurtPlayer(true);
  }

  function updatePlayer(input, dt) {
    const accel = input.dash ? 0.66 : 0.48;
    const maxSpeed = input.dash ? 5.3 : 4.1;

    if (input.left) {
      player.vx -= accel * dt;
      player.facing = -1;
    }
    if (input.right) {
      player.vx += accel * dt;
      player.facing = 1;
    }
    if (!input.left && !input.right) {
      player.vx *= Math.pow(0.82, dt);
      if (Math.abs(player.vx) < 0.04) player.vx = 0;
    }

    player.vx = clamp(player.vx, -maxSpeed, maxSpeed);

    if (input.jump && player.grounded) {
      player.vy = -12.4;
      player.grounded = false;
      player.jumpHold = 11;
      beep(520, 0.09, "square", 0.05);
      puff(player.x + player.w / 2, player.y + player.h, "#d9f1ff", 5);
    }

    if (input.jump && player.jumpHold > 0 && player.vy < 0) {
      player.vy -= 0.25 * dt;
      player.jumpHold -= dt;
    } else {
      player.jumpHold = 0;
    }

    player.vy = Math.min(MAX_FALL, player.vy + GRAVITY * dt);
    moveEntity(player, dt, true);
    player.x = clamp(player.x, 0, WORLD_W - player.w);
    if (player.invuln > 0) player.invuln -= dt;

    collectCoins();
    hitHazards();
    hitEnemies();
    if (intersects(player, flag)) winGame();
  }

  function moveEntity(entity, dt, canHitBlocks) {
    entity.x += entity.vx * dt;
    resolveAxis(entity, "x", canHitBlocks);
    entity.y += entity.vy * dt;
    entity.grounded = false;
    resolveAxis(entity, "y", canHitBlocks);
  }

  function solidList(canHitBlocks) {
    const solids = platforms.slice();
    if (canHitBlocks) {
      for (const block of blocks) solids.push(block);
    }
    return solids;
  }

  function resolveAxis(entity, axis, canHitBlocks) {
    for (const solid of solidList(canHitBlocks)) {
      if (!intersects(entity, solid)) continue;
      if (axis === "x") {
        if (entity.vx > 0) entity.x = solid.x - entity.w;
        if (entity.vx < 0) entity.x = solid.x + solid.w;
        entity.vx = 0;
      } else {
        if (entity.vy > 0) {
          entity.y = solid.y - entity.h;
          entity.vy = 0;
          entity.grounded = true;
        } else if (entity.vy < 0) {
          entity.y = solid.y + solid.h;
          entity.vy = 0;
          if (solid.type) bumpBlock(solid);
        }
      }
    }
  }

  function bumpBlock(block) {
    if (block.used) {
      block.bump = 8;
      beep(130, 0.05, "square", 0.025);
      return;
    }
    block.used = true;
    block.bump = 14;
    if (block.type === "coin") {
      addScore(100, block.x + 8, block.y - 8);
      addCoin(block.x + 16, block.y - 8);
    } else if (block.type === "gem") {
      addScore(500, block.x + 8, block.y - 8);
      coins += 5;
      burst(block.x + 16, block.y + 8, "#7de1ff", 14);
      beep(780, 0.14, "triangle", 0.065);
      updateHud();
    } else if (block.type === "spring") {
      player.vy = -15.5;
      burst(block.x + 16, block.y, "#ffcf45", 10);
      beep(340, 0.12, "sawtooth", 0.045);
    }
  }

  function addCoin(x, y) {
    coins += 1;
    addScore(100, x, y);
    burst(x, y, "#ffd84d", 8);
    beep(880, 0.08, "triangle", 0.045);
    updateHud();
    if (coins >= 100) {
      coins -= 100;
      lives += 1;
      beep(1040, 0.22, "square", 0.05);
      updateHud();
    }
  }

  function addScore(value, x, y) {
    score += value;
    floatingText.push({ x, y, text: "+" + value, life: 54 });
    updateHud();
  }

  function collectCoins() {
    for (const coin of coinItems) {
      if (!coin.taken && intersects(player, coin)) {
        coin.taken = true;
        addCoin(coin.x, coin.y);
      }
    }
  }

  function hitHazards() {
    for (const hazard of hazards) {
      if (intersects(player, hazard)) hurtPlayer(false);
    }
  }

  function hitEnemies() {
    for (const enemy of enemies) {
      if (!enemy.alive || enemy.squash > 0 || !intersects(player, enemy)) continue;
      const stomp = player.vy > 0 && player.y + player.h - enemy.y < 18;
      if (stomp) {
        enemy.squash = 22;
        enemy.vx = 0;
        player.vy = -9.2;
        addScore(200, enemy.x, enemy.y);
        burst(enemy.x + enemy.w / 2, enemy.y + 10, "#f5d36a", 10);
        beep(240, 0.09, "square", 0.05);
      } else {
        hurtPlayer(false);
      }
    }
  }

  function hurtPlayer(force) {
    if (!force && player.invuln > 0) return;
    lives -= 1;
    updateHud();
    burst(player.x + player.w / 2, player.y + player.h / 2, "#e34e45", 18);
    beep(96, 0.24, "sawtooth", 0.055);
    if (lives <= 0) {
      gameOver = true;
      showOverlay("游戏结束", "重开");
      return;
    }
    player.x = player.spawnX;
    player.y = player.spawnY;
    player.vx = 0;
    player.vy = 0;
    player.invuln = 110;
    camera = 0;
  }

  function winGame() {
    won = true;
    score += Math.ceil(timer) * 10;
    updateHud();
    beep(660, 0.12, "triangle", 0.055);
    setTimeout(() => beep(880, 0.14, "triangle", 0.05), 120);
    showOverlay("通关", "再来");
  }

  function showOverlay(title, buttonText) {
    overlay.querySelector("h1").textContent = title;
    startButton.textContent = buttonText;
    overlay.classList.remove("hidden");
  }

  function updateEnemies(dt) {
    for (const enemy of enemies) {
      if (!enemy.alive) continue;
      if (enemy.squash > 0) {
        enemy.squash -= dt;
        if (enemy.squash <= 0) enemy.alive = false;
        continue;
      }
      enemy.vy = Math.min(MAX_FALL, enemy.vy + GRAVITY * dt);
      moveEntity(enemy, dt, false);
      if (enemy.x < enemy.minX || enemy.x + enemy.w > enemy.maxX) {
        enemy.vx *= -1;
        enemy.x = clamp(enemy.x, enemy.minX, enemy.maxX - enemy.w);
      }
    }
  }

  function updateItems(dt) {
    for (const block of blocks) {
      if (block.bump > 0) block.bump = Math.max(0, block.bump - dt);
    }
    for (const coin of coinItems) {
      coin.spin += 0.08 * dt;
    }
  }

  function burst(x, y, color, count) {
    for (let i = 0; i < count; i += 1) {
      particles.push({
        x,
        y,
        vx: (Math.random() - 0.5) * 5,
        vy: -Math.random() * 5 - 1,
        life: 28 + Math.random() * 18,
        color,
      });
    }
  }

  function puff(x, y, color, count) {
    for (let i = 0; i < count; i += 1) {
      particles.push({
        x: x + (Math.random() - 0.5) * 22,
        y: y + Math.random() * 5,
        vx: (Math.random() - 0.5) * 1.2,
        vy: -Math.random() * 1.4,
        life: 18 + Math.random() * 10,
        color,
      });
    }
  }

  function updateParticles(dt) {
    for (const p of particles) {
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.vy += 0.18 * dt;
      p.life -= dt;
    }
    particles = particles.filter((p) => p.life > 0);
    for (const text of floatingText) {
      text.y -= 0.55 * dt;
      text.life -= dt;
    }
    floatingText = floatingText.filter((text) => text.life > 0);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    drawSky();
    ctx.save();
    ctx.translate(-Math.floor(camera), 0);
    drawWorldBack();
    drawPlatforms();
    drawBlocks();
    drawCoins();
    drawHazards();
    drawFlag();
    drawEnemies();
    drawPlayer();
    drawParticles();
    ctx.restore();
    if (paused && !gameOver && !won) drawPause();
  }

  function drawSky() {
    const grad = ctx.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, "#76cfff");
    grad.addColorStop(0.58, "#b7ecff");
    grad.addColorStop(1, "#8ed46e");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = "rgba(255,255,255,0.72)";
    cloud(120 - camera * 0.12, 86, 1.2);
    cloud(440 - camera * 0.09, 122, 0.8);
    cloud(810 - camera * 0.14, 72, 1.0);
    cloud(1180 - camera * 0.1, 116, 0.9);
  }

  function cloud(x, y, s) {
    const wrap = W + 280;
    const sx = ((x % wrap) + wrap) % wrap - 120;
    ctx.fillRect(sx, y + 22 * s, 92 * s, 16 * s);
    ctx.beginPath();
    ctx.arc(sx + 18 * s, y + 22 * s, 22 * s, 0, Math.PI * 2);
    ctx.arc(sx + 44 * s, y + 12 * s, 30 * s, 0, Math.PI * 2);
    ctx.arc(sx + 74 * s, y + 22 * s, 22 * s, 0, Math.PI * 2);
    ctx.fill();
  }

  function drawWorldBack() {
    for (let x = 0; x < WORLD_W; x += 384) {
      ctx.fillStyle = "#5ca35d";
      ctx.beginPath();
      ctx.moveTo(x, GROUND_Y);
      ctx.lineTo(x + 144, GROUND_Y - 112);
      ctx.lineTo(x + 288, GROUND_Y);
      ctx.fill();
      ctx.fillStyle = "rgba(255,255,255,0.16)";
      ctx.fillRect(x + 138, GROUND_Y - 98, 20, 18);
    }
  }

  function drawPlatforms() {
    for (const p of platforms) {
      const top = p.y < GROUND_Y;
      ctx.fillStyle = top ? palettes.grass[0] : palettes.earth[0];
      ctx.fillRect(p.x, p.y, p.w, p.h);
      if (top || p.y === GROUND_Y) {
        ctx.fillStyle = palettes.grass[0];
        ctx.fillRect(p.x, p.y, p.w, 8);
        ctx.fillStyle = palettes.grass[1];
        ctx.fillRect(p.x, p.y + 8, p.w, 5);
      }
      ctx.fillStyle = palettes.earth[1];
      ctx.fillRect(p.x, p.y + 16, p.w, p.h - 16);
      ctx.fillStyle = palettes.earth[2];
      ctx.fillRect(p.x + 4, p.y + 22, 8, 8);
      ctx.fillRect(p.x + 20, p.y + 38, 8, 8);
    }
  }

  function drawBlocks() {
    for (const b of blocks) {
      const y = b.y - Math.sin((b.bump / 14) * Math.PI) * b.bump;
      if (b.used) {
        ctx.fillStyle = "#8a755e";
        ctx.fillRect(b.x, y, b.w, b.h);
        ctx.fillStyle = "#6c584a";
        ctx.fillRect(b.x + 5, y + 5, b.w - 10, b.h - 10);
      } else {
        ctx.fillStyle = b.type === "spring" ? "#63d4c8" : palettes.crate[0];
        ctx.fillRect(b.x, y, b.w, b.h);
        ctx.fillStyle = palettes.crate[1];
        ctx.fillRect(b.x + 3, y + 3, b.w - 6, 5);
        ctx.fillRect(b.x + 3, y + b.h - 8, b.w - 6, 5);
        ctx.fillRect(b.x + 3, y + 3, 5, b.h - 6);
        ctx.fillRect(b.x + b.w - 8, y + 3, 5, b.h - 6);
        ctx.fillStyle = b.type === "gem" ? "#7de1ff" : "#fff2a1";
        star(b.x + 16, y + 16, 9);
      }
    }
  }

  function star(x, y, r) {
    ctx.beginPath();
    for (let i = 0; i < 10; i += 1) {
      const a = -Math.PI / 2 + (i * Math.PI) / 5;
      const rr = i % 2 ? r * 0.45 : r;
      const px = x + Math.cos(a) * rr;
      const py = y + Math.sin(a) * rr;
      if (i === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    }
    ctx.closePath();
    ctx.fill();
  }

  function drawCoins() {
    for (const c of coinItems) {
      if (c.taken) continue;
      const sw = Math.max(4, Math.abs(Math.cos(c.spin)) * 14);
      ctx.fillStyle = "#ffd84d";
      ctx.fillRect(c.x + (18 - sw) / 2, c.y, sw, 18);
      ctx.fillStyle = "#fff3a7";
      ctx.fillRect(c.x + 7, c.y + 3, 3, 12);
    }
  }

  function drawHazards() {
    for (const h of hazards) {
      ctx.fillStyle = "#4b5967";
      ctx.fillRect(h.x, h.y + 12, h.w, 6);
      for (let x = h.x; x < h.x + h.w; x += 16) {
        ctx.fillStyle = "#e7edf2";
        ctx.beginPath();
        ctx.moveTo(x, h.y + 18);
        ctx.lineTo(x + 8, h.y);
        ctx.lineTo(x + 16, h.y + 18);
        ctx.fill();
      }
    }
  }

  function drawFlag() {
    ctx.fillStyle = "#4d3b31";
    ctx.fillRect(flag.x + 9, flag.y, 6, flag.h);
    ctx.fillStyle = "#2fc3b3";
    ctx.fillRect(flag.x + 15, flag.y + 18, 88, 44);
    ctx.fillStyle = "#fff5c0";
    star(flag.x + 45, flag.y + 40, 12);
    ctx.fillStyle = "#6d432b";
    ctx.fillRect(flag.x - 10, flag.y + flag.h - 12, 44, 12);
  }

  function drawEnemies() {
    for (const e of enemies) {
      if (!e.alive) continue;
      const h = e.squash > 0 ? 14 : e.h;
      const y = e.y + (e.h - h);
      ctx.fillStyle = palettes.enemy[0];
      ctx.fillRect(e.x, y + 8, e.w, h - 8);
      ctx.fillStyle = palettes.enemy[1];
      ctx.fillRect(e.x + 3, y + h - 6, 9, 6);
      ctx.fillRect(e.x + e.w - 12, y + h - 6, 9, 6);
      ctx.fillStyle = palettes.enemy[2];
      ctx.fillRect(e.x + 7, y + 12, 5, 5);
      ctx.fillRect(e.x + 18, y + 12, 5, 5);
    }
  }

  function drawPlayer() {
    const blink = player.invuln > 0 && Math.floor(player.invuln / 8) % 2 === 0;
    if (blink) return;
    const x = Math.floor(player.x);
    const y = Math.floor(player.y);
    const flip = player.facing < 0;

    ctx.save();
    ctx.translate(x + (flip ? player.w : 0), y);
    ctx.scale(flip ? -1 : 1, 1);
    ctx.fillStyle = palettes.hero[4];
    ctx.fillRect(7, 18, 17, 24);
    ctx.fillStyle = palettes.hero[1];
    ctx.fillRect(7, 28, 9, 18);
    ctx.fillRect(17, 28, 9, 18);
    ctx.fillStyle = palettes.hero[2];
    ctx.fillRect(8, 8, 18, 16);
    ctx.fillStyle = palettes.hero[0];
    ctx.fillRect(5, 3, 22, 8);
    ctx.fillRect(16, 0, 13, 6);
    ctx.fillStyle = palettes.hero[3];
    ctx.fillRect(20, 13, 4, 4);
    ctx.fillRect(13, 22, 8, 3);
    ctx.fillStyle = "#f7d28f";
    ctx.fillRect(2, 21, 7, 12);
    ctx.fillRect(23, 21, 7, 12);
    ctx.fillStyle = "#2b2442";
    ctx.fillRect(5, 44, 10, 4);
    ctx.fillRect(18, 44, 10, 4);
    ctx.restore();
  }

  function drawParticles() {
    for (const p of particles) {
      ctx.globalAlpha = clamp(p.life / 30, 0, 1);
      ctx.fillStyle = p.color;
      ctx.fillRect(p.x, p.y, 5, 5);
      ctx.globalAlpha = 1;
    }

    ctx.font = "14px ui-monospace, monospace";
    ctx.textAlign = "center";
    for (const t of floatingText) {
      ctx.globalAlpha = clamp(t.life / 32, 0, 1);
      ctx.fillStyle = "#fff8c8";
      ctx.fillText(t.text, t.x, t.y);
      ctx.globalAlpha = 1;
    }
  }

  function drawPause() {
    ctx.fillStyle = "rgba(12, 18, 28, 0.45)";
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "#fff5c0";
    ctx.font = "700 44px ui-monospace, monospace";
    ctx.textAlign = "center";
    ctx.fillText("暂停", W / 2, H / 2);
  }

  window.addEventListener("keydown", (event) => {
    if (["ArrowLeft", "ArrowRight", "ArrowUp", "Space"].includes(event.code)) event.preventDefault();
    keys.add(event.code);
    if (event.code === "KeyP" && running && !gameOver && !won) paused = !paused;
    if (event.code === "KeyR") startGame();
  });

  window.addEventListener("keyup", (event) => {
    keys.delete(event.code);
  });

  document.querySelectorAll(".touch-btn").forEach((btn) => {
    const key = btn.dataset.key;
    const down = (event) => {
      event.preventDefault();
      touch[key] = true;
    };
    const up = (event) => {
      event.preventDefault();
      touch[key] = false;
    };
    btn.addEventListener("pointerdown", down);
    btn.addEventListener("pointerup", up);
    btn.addEventListener("pointercancel", up);
    btn.addEventListener("pointerleave", up);
  });

  startButton.addEventListener("click", startGame);
  resetGame();
  draw();
}());
