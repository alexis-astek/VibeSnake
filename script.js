(function () {
  'use strict';

  // Config
  const canvas = document.getElementById('game');
  const ctx = canvas.getContext('2d');
  const gridSize = 20; // 32px cells on 640px -> 20x20
  const cellPx = canvas.width / gridSize; // must be integer for crisp text
  const tickMs = 120; // game speed

  const letters = ['S', 'N', 'A', 'K', 'E'];

  // Game state
  let snake; // array of {x,y,letter|null}
  let dir; // {x,y} current direction
  let nextDir; // buffered direction to avoid reversing instantly
  let foods; // array of {x,y,letter}
  let nextLetterIndex; // index into letters for required pickup
  let score;
  let running = true;
  let gameOver = false;
  let loopHandle = null;

  // UI elements
  const scoreEl = document.getElementById('score');
  const nextEl = document.getElementById('next');
  const overlay = document.getElementById('overlay');
  const overlayTitle = document.getElementById('overlay-title');
  const overlayBody = document.getElementById('overlay-body');
  const restartBtn = document.getElementById('restart');

  function init() {
    const startX = Math.floor(gridSize / 2);
    const startY = Math.floor(gridSize / 2);
    snake = [
      { x: startX, y: startY, letter: null },
      { x: startX - 1, y: startY, letter: null },
      { x: startX - 2, y: startY, letter: null }
    ];
    dir = { x: 1, y: 0 };
    nextDir = { x: 1, y: 0 };
    nextLetterIndex = 0;
    score = 0;
    foods = [];
    spawnFoods();
    updateHUD();
    gameOver = false;
    running = true;
    hideOverlay();
    if (loopHandle) clearInterval(loopHandle);
    loopHandle = setInterval(tick, tickMs);
    draw();
  }

  function gridKey(x, y) { return x + ':' + y; }

  function spawnFoods() {
    // Ensure 5 foods always present, letters S N A K E in random positions, unique positions not on snake
    const occupied = new Set(snake.map(s => gridKey(s.x, s.y)));
    foods = [];
    for (let i = 0; i < letters.length; i++) {
      let pos;
      do {
        pos = { x: randInt(0, gridSize - 1), y: randInt(0, gridSize - 1) };
      } while (occupied.has(gridKey(pos.x, pos.y)) || foods.some(f => f.x === pos.x && f.y === pos.y));
      foods.push({ x: pos.x, y: pos.y, letter: letters[i] });
    }
  }

  function randInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

  function tick() {
    if (!running || gameOver) return;
    // apply buffered direction
    if (!isOpposite(nextDir, dir)) dir = nextDir;

    const head = snake[0];
    const newHead = { x: head.x + dir.x, y: head.y + dir.y, letter: null };

    // wall collision
    if (newHead.x < 0 || newHead.x >= gridSize || newHead.y < 0 || newHead.y >= gridSize) {
      return endGame('You hit the wall.');
    }

    // self collision (with head entering a cell occupied by body)
    for (let i = 0; i < snake.length; i++) {
      if (snake[i].x === newHead.x && snake[i].y === newHead.y) {
        return endGame('You bit yourself.');
      }
    }

    // move: add head
    snake.unshift(newHead);

    // food check: must match next required letter
    const targetLetter = letters[nextLetterIndex];
    const eatenIndex = foods.findIndex(f => f.x === newHead.x && f.y === newHead.y && f.letter === targetLetter);

    if (eatenIndex !== -1) {
      // Eat correct letter
      const eatenFood = foods[eatenIndex];
      snake[0].letter = eatenFood.letter; // the new head carries the letter
      score += 10;
      nextLetterIndex = (nextLetterIndex + 1) % letters.length;
      // respawn just the eaten food anywhere not occupied
      const occupied = new Set(snake.map(s => gridKey(s.x, s.y)).concat(foods.map(f => gridKey(f.x, f.y))));
      let pos;
      do {
        pos = { x: randInt(0, gridSize - 1), y: randInt(0, gridSize - 1) };
      } while (occupied.has(gridKey(pos.x, pos.y)));
      foods[eatenIndex] = { x: pos.x, y: pos.y, letter: eatenFood.letter };
    } else {
      // no food eaten: remove tail
      snake.pop();
    }

    updateHUD();
    draw();
  }

  function endGame(reason) {
    gameOver = true;
    running = false;
    showOverlay('Game Over', reason + ' Press R to restart.');
  }

  function updateHUD() {
    scoreEl.textContent = String(score);
    nextEl.textContent = letters[nextLetterIndex];
  }

  function draw() {
    // clear board
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // draw foods
    for (const f of foods) drawCell(f.x, f.y, '#2b2f5a');
    for (const f of foods) drawLetter(f.x, f.y, f.letter, getFoodColor(f.letter));

    // draw snake
    for (let i = snake.length - 1; i >= 0; i--) {
      const seg = snake[i];
      const base = i === 0 ? '#6cf0a5' : '#45e695';
      const stroke = i === 0 ? '#32d583' : '#28c76f';
      drawCell(seg.x, seg.y, base, stroke);
    }
    // draw letters on snake segments that have a letter
    for (const seg of snake) {
      if (seg.letter) drawLetter(seg.x, seg.y, seg.letter, '#0a2d1c');
    }

    // draw head indicator (eyes)
    drawEyes();
  }

  function drawCell(x, y, fill, stroke) {
    const px = x * cellPx;
    const py = y * cellPx;
    ctx.fillStyle = fill;
    ctx.strokeStyle = stroke || 'rgba(255,255,255,0.12)';
    ctx.lineWidth = Math.max(2, cellPx * 0.06);
    roundRect(ctx, px + 3, py + 3, cellPx - 6, cellPx - 6, Math.min(8, cellPx * 0.2), true, true);
  }

  function drawLetter(x, y, letter, color) {
    const px = x * cellPx;
    const py = y * cellPx;
    ctx.fillStyle = color || 'white';
    ctx.font = `${Math.floor(cellPx * 0.55)}px Inter, system-ui, sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(letter, px + cellPx / 2, py + cellPx / 2 + 1);
  }

  function drawEyes() {
    const head = snake[0];
    const cx = head.x * cellPx + cellPx / 2;
    const cy = head.y * cellPx + cellPx / 2;
    const offset = cellPx * 0.18;
    const r = Math.max(2, cellPx * 0.07);
    ctx.fillStyle = '#0b1b30';
    if (dir.x !== 0) {
      circle(cx, cy - offset, r);
      circle(cx, cy + offset, r);
    } else {
      circle(cx - offset, cy, r);
      circle(cx + offset, cy, r);
    }
  }

  function circle(cx, cy, r) {
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI * 2);
    ctx.fill();
  }

  function roundRect(ctx2d, x, y, w, h, r, fill, stroke) {
    if (w < 2 * r) r = w / 2;
    if (h < 2 * r) r = h / 2;
    ctx2d.beginPath();
    ctx2d.moveTo(x + r, y);
    ctx2d.arcTo(x + w, y, x + w, y + h, r);
    ctx2d.arcTo(x + w, y + h, x, y + h, r);
    ctx2d.arcTo(x, y + h, x, y, r);
    ctx2d.arcTo(x, y, x + w, y, r);
    ctx2d.closePath();
    if (fill) ctx2d.fill();
    if (stroke) ctx2d.stroke();
  }

  function getFoodColor(letter) {
    switch (letter) {
      case 'S': return '#f59e0b';
      case 'N': return '#f97316';
      case 'A': return '#fb7185';
      case 'K': return '#a78bfa';
      case 'E': return '#38bdf8';
      default: return '#f59e0b';
    }
  }

  function isOpposite(a, b) { return a.x === -b.x && a.y === -b.y; }

  // Input
  const keyDir = {
    ArrowUp: { x: 0, y: -1 }, KeyW: { x: 0, y: -1 },
    ArrowDown: { x: 0, y: 1 }, KeyS: { x: 0, y: 1 },
    ArrowLeft: { x: -1, y: 0 }, KeyA: { x: -1, y: 0 },
    ArrowRight: { x: 1, y: 0 }, KeyD: { x: 1, y: 0 }
  };

  window.addEventListener('keydown', (e) => {
    if (e.code in keyDir) {
      const nd = keyDir[e.code];
      // prevent reversing directly into neck
      if (!isOpposite(nd, dir)) nextDir = nd;
      e.preventDefault();
    } else if (e.code === 'KeyP') {
      togglePause();
      e.preventDefault();
    } else if (e.code === 'KeyR') {
      init();
      e.preventDefault();
    }
  });

  restartBtn.addEventListener('click', () => init());

  function togglePause() {
    if (gameOver) return;
    running = !running;
    if (running) {
      hideOverlay();
    } else {
      showOverlay('Paused', 'Press P to resume');
    }
  }

  function showOverlay(title, body) {
    overlayTitle.textContent = title;
    overlayBody.textContent = body;
    overlay.classList.remove('hidden');
  }
  function hideOverlay() { overlay.classList.add('hidden'); }

  // Start
  init();
})();


