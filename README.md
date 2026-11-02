# CodeFlow — Interactive DSA Visualizer

**See the logic. Trace every step.**

CodeFlow is a portfolio-ready learning tool for visualizing core data structures and algorithms. It combines a React + TypeScript frontend with a FastAPI backend. The frontend also works without the backend for the core visualizations.

## Features
- Sorting: Bubble, Selection, Insertion, Merge and Quick Sort with step-by-step traces.
- Linked list: insert at head/tail, delete by value, search, reverse, and remove duplicates (LeetCode 83).
- Stack and queue operations with empty/full checks.
- Binary search trace with left/mid/right pointers.
- Challenge mode with built-in questions and answer checking.
- Progress and bookmarks saved in browser localStorage.
- Export/import progress JSON.
- FastAPI health and algorithm endpoints.
- Responsive dark UI, keyboard-friendly controls, custom arrays, playback speed, and reset.

## Stack
- Frontend: React, TypeScript, Vite, CSS
- Backend: Python 3.11+, FastAPI, Pydantic, Uvicorn, pytest

## Run locally

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

### 2. Frontend
Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the URL Vite prints (usually http://localhost:5173).

The frontend calls the API only for the API status panel; the main visualizations run locally so the learning experience doesn't depend on a server connection.

## Tests
```bash
cd backend
pytest
```

## Project structure
```text
codeflow/
├── backend/
│   ├── app/main.py
│   ├── requirements.txt
│   └── tests/test_algorithms.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── algorithms.ts
│       └── styles.css
├── LICENSE
└── .gitignore
```

## Complexity quick reference

| Algorithm / operation | Time | Extra space |
|---|---:|---:|
| Bubble sort | O(n²) | O(1) |
| Selection sort | O(n²) | O(1) |
| Insertion sort | O(n²) | O(1) |
| Merge sort | O(n log n) | O(n) |
| Quick sort | O(n log n) average, O(n²) worst | O(log n) average |
| Binary search | O(log n) | O(1) iterative |
| Linked-list search | O(n) | O(1) |
| Remove duplicates from sorted list | O(n) | O(1) |
| Stack push/pop/peek | O(1) | O(1) per operation |
| Queue enqueue/dequeue | O(1) with a deque | O(1) per operation |

## GitHub publishing
Create a new empty GitHub repository named `codeflow-dsa-visualizer`, then run from this folder:
```bash
git init
git add .
git commit -m "Build CodeFlow DSA visualizer"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/codeflow-dsa-visualizer.git
git push -u origin main
```
Replace `YOUR_USERNAME` with your GitHub username. Never commit secrets or access tokens.

## Notes
- Progress is stored in this browser using localStorage; it is not synced between devices.
- The FastAPI service currently provides stateless algorithm endpoints and a health check. Authentication and cloud user accounts are intentionally not included.
- Add screenshots to `docs/screenshots/` after running the app; don't commit fabricated screenshots.
