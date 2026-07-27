import random
import time
from collections import deque

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Engineering Systems Qualification", page_icon="🛠️", layout="wide")

ROWS, COLS = 21, 31


def carve_maze(rows: int, cols: int, seed: int):
    rng = random.Random(seed)
    grid = [[1 for _ in range(cols)] for _ in range(rows)]
    stack = [(1, 1)]
    grid[1][1] = 0
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    while stack:
        r, c = stack[-1]
        choices = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and grid[nr][nc] == 1:
                choices.append((nr, nc, dr, dc))
        if choices:
            nr, nc, dr, dc = rng.choice(choices)
            grid[r + dr // 2][c + dc // 2] = 0
            grid[nr][nc] = 0
            stack.append((nr, nc))
        else:
            stack.pop()

    return grid


def farthest_open_cell(grid, start):
    q = deque([(start, 0)])
    seen = {start}
    farthest = start
    max_dist = 0
    while q:
        (r, c), dist = q.popleft()
        if dist > max_dist:
            farthest, max_dist = (r, c), dist
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0 and (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append(((nr, nc), dist + 1))
    return farthest


def new_game():
    seed = random.randint(1, 999999)
    maze = carve_maze(ROWS, COLS, seed)
    start = (1, 1)
    goal = farthest_open_cell(maze, start)
    st.session_state.maze_seed = seed
    st.session_state.maze = maze
    st.session_state.player = start
    st.session_state.goal = goal
    st.session_state.moves = 0
    st.session_state.bump_count = 0
    st.session_state.started_at = time.time()
    st.session_state.finished = False
    st.session_state.message = "Assessment initialized. Locate the final approval terminal."


if "maze" not in st.session_state:
    new_game()

maze = st.session_state.maze
player = st.session_state.player
goal = st.session_state.goal

st.markdown("""
<style>
.stApp { background: #eef3f8; }
.block-container { max-width: 1450px; padding-top: 1rem; }
.hero { background: linear-gradient(135deg,#0b2742,#174f78); color:white; padding:20px 26px; border-radius:14px; box-shadow:0 8px 22px rgba(0,0,0,.15); }
.kicker { letter-spacing:.18em; font-size:.75rem; opacity:.75; font-weight:700; }
.panel {
    background:#2b2d31;
    border:1px solid #42464d;
    border-radius:14px;
    padding:18px;
}
..metric-label {
    color:##607286 !important;
    font-size:.75rem;
    text-transform:uppercase;
    letter-spacing:.08em;
}

.metric-value {
    color:#102f4c !important;
    font-size:1.5rem;
    font-weight:800;
}
.maze { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; line-height:1; font-size:20px; background:#081a2b; border:7px solid #173f5f; border-radius:12px; padding:14px; overflow:auto; text-align:center; }
.wall { color:#4f7598; }
.path { color:#10263a; }
.player { color:#ffd166; text-shadow:0 0 8px #ffd166; }
.goal { color:#66e3a4; text-shadow:0 0 8px #66e3a4; }
.critter { color:#f8b4d9; }
.alert {background:#e6e6e6; /* optional gray background */ border-left:5px solid #000000; color:#000000; }
</style>
""", unsafe_allow_html=True)

st.markdown("""

<div class="hero">
<div class="kicker">BENCHMARK INTERNAL TRAINING PORTAL</div>
<h1 style="margin:.2rem 0">Manufacturing Process Navigation Assessment</h1>
<div>Candidate module: Engineering Systems Qualification • Revision 2.1 • CAT-ITICAL risk classification</div>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([3.1, 1], gap="large")

with right:
    elapsed = int(time.time() - st.session_state.started_at)
    mins, secs = divmod(elapsed, 60)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("""
<div style="
background:#174f78;
padding:15px;
border-radius:12px;
margin-bottom:10px;
">
<h3 style="color:#e8edf2;margin:0;">
Qualification Status
</h3>
</div>
""", unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Moves logged</div><div class="metric-value">{st.session_state.moves}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Process deviations</div><div class="metric-value">{st.session_state.bump_count}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Elapsed time</div><div class="metric-value">{mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Risk level</div><div class="metric-value">CAT-ITICAL 🐈</div>', unsafe_allow_html=True)
    st.progress(min(0.95, st.session_state.moves / 250), text="Approval routing progress")
    st.markdown("**Controls:** arrow buttons or WASD input below")
    if st.button("Generate New Assessment", use_container_width=True):
        new_game()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with left:
    if st.session_state.finished:
        st.success("Final approval terminal reached. Mandatory audiovisual training unlocked.")
        st.balloons()
        components.html("""
        <div style="background:#081a2b;color:gray;padding:24px;border-radius:14px;text-align:center;font-family:Arial">
          <h1>✅ ENGINEERING QUALIFICATION COMPLETE</h1>
          <p>Your final required module is: <b>Never Gonna Give You Up — Process Commitment Training</b></p>
          <iframe width="760" height="428" src="https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1" title="Mandatory training" frameborder="0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>
          <p style="opacity:.7">Failure to complete the full module may require maze requalification.</p>
        </div>
        """, height=560)
    else:
        critters = {}
        open_cells = [(r, c) for r in range(ROWS) for c in range(COLS) if maze[r][c] == 0 and (r, c) not in (player, goal, (1, 1))]
        rng = random.Random(st.session_state.maze_seed)
        for cell in rng.sample(open_cells, min(10, len(open_cells))):
            critters[cell] = rng.choice(["🐈", "🐈‍⬛", "🦫", "🐾"])

        lines = []
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                if (r, c) == player:
                    row.append('<span class="player">●</span>')
                elif (r, c) == goal:
                    row.append('<span class="goal">◆</span>')
                elif (r, c) in critters:
                    row.append(f'<span class="critter">{critters[(r,c)]}</span>')
                elif maze[r][c] == 1:
                    row.append('<span class="wall">██</span>')
                else:
                    row.append('<span class="path">··</span>')
            lines.append("".join(row))
        st.markdown('<div class="maze">' + '<br>'.join(lines) + '</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="alert"><b>System message:</b> {st.session_state.message}</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            up = st.button("⬆️ UP / W", use_container_width=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            left_btn = st.button("⬅️ LEFT / A", use_container_width=True)
        with c2:
            down = st.button("⬇️ DOWN / S", use_container_width=True)
        with c3:
            right_btn = st.button("➡️ RIGHT / D", use_container_width=True)

        if "kbd_nonce" not in st.session_state:
            st.session_state.kbd_nonce = 0
        key_press = st.text_input("Keyboard command", placeholder="Type W, A, S, or D and press Enter", max_chars=1, label_visibility="collapsed", key=f"kbd_input_{st.session_state.kbd_nonce}").lower()

        drdc = None
        if up or key_press == "W": drdc = (-1, 0)
        elif down or key_press == "S": drdc = (1, 0)
        elif left_btn or key_press == "A": drdc = (0, -1)
        elif right_btn or key_press == "D": drdc = (0, 1)

        if drdc:
            nr, nc = player[0] + drdc[0], player[1] + drdc[1]
            st.session_state.moves += 1
            if maze[nr][nc] == 0:
                st.session_state.player = (nr, nc)
                if (nr, nc) == goal:
                    st.session_state.finished = True
                elif (nr, nc) in critters:
                    st.session_state.message = random.choice([
                        "Capybara consultant acknowledges your routing choice.",
                        "Cat auditor detected. Maintain professional composure.",
                        "Unexpected animal-based stakeholder approval received.",
                    ])
                else:
                    st.session_state.message = random.choice([
                        "Routing accepted. Continue through the approval matrix.",
                        "No nonconformance detected. Proceed.",
                        "Path validated by imaginary engineering.",
                        "Documentation review remains unnecessarily complicated.",
                    ])
            else:
                st.session_state.bump_count += 1
                st.session_state.message = random.choice([
                    "PROCESS DEVIATION: You attempted to enter an undocumented work cell.",
                    "Access denied. Submit a TAF form and try another route.",
                    "Wall contact recorded. Quality has been copied on the email.",
                    "Invalid move. The cat auditor appears disappointed.",
                ])
            if key_press:
                st.session_state.kbd_nonce += 1
            st.rerun()

st.caption("For entertainment only. No interns, cats, capybaras, or quality systems were harmed during validation.")
