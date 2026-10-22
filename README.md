# Tic Tac Toe AI

A responsive Tic Tac Toe game where you play as **X** against an AI opponent (**O**) powered by the **Minimax algorithm**. The frontend uses HTML, CSS and JavaScript; the backend uses Python and Flask.

## Features

- Responsive, modern dark UI
- Human vs AI gameplay
- Minimax AI that plays optimally
- Win, loss and draw counters
- New game and reset score controls
- Backend API endpoint for AI moves
- Basic input validation on the server

## Tech stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend structure | HTML5 | Game layout and accessible controls |
| Styling | CSS3 | Responsive visual design |
| Frontend behavior | JavaScript | Board interaction and API calls |
| Backend | Python + Flask | Serves the page and AI endpoint |
| AI algorithm | Minimax | Searches possible moves to choose an optimal move |

## Project structure

```text
tic_tac_toe_ai/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

6. Open **http://127.0.0.1:5000** in your browser.

## How the AI works

The Minimax algorithm explores possible future board states. It scores an AI win as `+1`, a human win as `-1`, and a draw as `0`. The AI selects the move with the best possible outcome assuming both sides play optimally. Tic Tac Toe has a small search space, so the full search is fast.

## API

### `POST /api/move`

Request JSON:

```json
{
  "board": ["X", "", "", "", "O", "", "", "", ""]
}
```

The board is an array of 9 strings. Each cell must be `"X"`, `"O"`, or `""`. The API returns the updated board, winner/game status and AI move index.

> This is a portfolio/demo project. For a public production deployment, add stronger turn-history validation, rate limiting, tests, and production server configuration.

## Possible improvements

- Add difficulty levels (easy, medium, hard)
- Add player-vs-player mode
- Add sound effects and animations
- Add automated unit tests
- Deploy using a production WSGI server
