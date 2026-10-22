const cells = [...document.querySelectorAll(".cell")];
const statusEl = document.querySelector("#status");
const winsEl = document.querySelector("#wins");
const lossesEl = document.querySelector("#losses");
const drawsEl = document.querySelector("#draws");
const humanScore = document.querySelector("#human-score");
const aiScore = document.querySelector("#ai-score");

let board = Array(9).fill("");
let busy = false;
let finished = false;
let scores = { wins: 0, losses: 0, draws: 0 };

function setStatus(message) { statusEl.textContent = message; }
function render() {
  cells.forEach((cell, i) => {
    cell.textContent = board[i];
    cell.classList.toggle("x", board[i] === "X");
    cell.classList.toggle("o", board[i] === "O");
    cell.disabled = busy || finished || board[i] !== "";
    cell.setAttribute("aria-label", `Square ${i + 1}${board[i] ? `, ${board[i]}` : ", empty"}`);
  });
  humanScore.classList.toggle("active", !busy && !finished);
  aiScore.classList.toggle("active", busy);
}
function winningLine(b) {
  const lines = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]];
  return lines.find(([a,c,d]) => b[a] && b[a] === b[c] && b[a] === b[d]) || null;
}
function finish(result) {
  finished = true;
  const line = winningLine(board);
  if (line) line.forEach(i => cells[i].classList.add("win"));
  if (result === "X") { scores.wins++; setStatus("You win! Great move."); }
  else if (result === "O") { scores.losses++; setStatus("AI wins this round. Try again!"); }
  else { scores.draws++; setStatus("It's a draw. Well played!"); }
  updateScores();
  render();
}
function updateScores() {
  winsEl.textContent = scores.wins;
  lossesEl.textContent = scores.losses;
  drawsEl.textContent = scores.draws;
}
async function play(index) {
  if (busy || finished || board[index]) return;
  board[index] = "X";
  if (winningLine(board)) { render(); finish("X"); return; }
  if (board.every(Boolean)) { render(); finish(null); return; }
  busy = true;
  setStatus("AI is thinking…");
  render();
  try {
    const response = await fetch("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Unable to get AI move.");
    board = data.board;
    busy = false;
    if (data.winner || data.draw || data.game_over) {
      finish(data.winner || null);
    } else {
      setStatus("Your turn — choose a square.");
      render();
    }
  } catch (error) {
    busy = false;
    setStatus("Connection issue. Please start a new game and try again.");
    console.error(error);
    render();
  }
}
function newGame() {
  board = Array(9).fill("");
  busy = false;
  finished = false;
  cells.forEach(c => c.classList.remove("win"));
  setStatus("Your turn — choose a square.");
  render();
}
cells.forEach((cell, index) => cell.addEventListener("click", () => play(index)));
document.querySelector("#new-game").addEventListener("click", newGame);
document.querySelector("#reset-score").addEventListener("click", () => {
  scores = { wins: 0, losses: 0, draws: 0 };
  updateScores();
  newGame();
});
render();
