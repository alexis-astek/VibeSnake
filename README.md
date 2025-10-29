# VibeSnake

A simple browser Snake game where the player collects the letters S, N, A, K, E as food.

## Gameplay
- Control the snake on a grid and eat food items.
- Food spawns as letters in sequence: S → N → A → K → E, then repeats.
- Each eaten letter increases length and score; completing SNAKE may add a small bonus.
- Hitting a wall or your own body ends the run.

## Controls
- Arrow keys: move
- Space/Enter: start or restart

## Files
- `index.html`: Canvas and UI
- `style.css`: Styling
- `script.js`: Game logic (movement, letter spawning, collisions, scoring)

## Run Locally
Open `index.html` directly, or serve the folder (e.g., `python -m http.server 8080`) and open `http://localhost:8080`.

## Deploy
Host on GitHub Pages. Set `PAGES_URL` to the live URL for automated testing.

## Project Automation (PoC)
- Bugs: `BUGS.md` with `Status`, `Versions`, `FixVersions`
- Versioning: `VERSION` holds integer N for release tag `V.N`
- Turn-taking: `PIPELINE_STATE.json` coordinates UI Tester → Dev → CICD
