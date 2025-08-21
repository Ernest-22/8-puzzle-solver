# 8-puzzle-solver
8-Puzzle Solver: Visualizes and compares A, DFS, IDS, and IDDFS with path cost, time, and nodes expanded

# 🧩 8-Puzzle Solver

An interactive **8-Puzzle Solver Web App** built with **Flask (Python backend)** and **JavaScript/HTML/CSS frontend**.  
The app allows users to shuffle, solve, and compare multiple search algorithms while visualizing the puzzle-solving process.

---

## 🚀 Features
- ✅ **Solve the 8-puzzle** using different search algorithms:
  - Iterative Deepening Search (IDS)
  - Depth-First Search (DFS)
  - Iterative Deepening Depth-First Search (IDDFS)
  - A* Search (with Misplaced Tiles heuristic)
- ✅ **Puzzle Validation**: Ensures only solvable puzzles can be played.
- ✅ **Shuffle & Reset Buttons** to generate random solvable puzzles.
- ✅ **Step-by-Step Solve Mode**: Watch the puzzle solve itself one move at a time.
- ✅ **Performance Comparison**: Compare algorithms based on:
  - Execution time
  - Number of nodes expanded
  - Solution path length
- ✅ **Responsive UI** with a clean, minimal design.

---

## 📸 Preview
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/cb512e9f-cb7d-4e9c-a0e4-9334901ff337" />
8-puzzle-solver/
│── static/          # CSS & JS files
│── templates/       # HTML files
│── app.py           # Flask backend
│── solver/          # Puzzle solver algorithms
│── README.md        # Project documentation

---

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript  
- **Backend:** Python (Flask)  
- **Algorithms Implemented:** IDS, DFS, IDDFS, A* (Misplaced Tiles)  

---

## ⚡ Getting Started

### 1️⃣ Clone the repository
```bash

git clone https://github.com/Ernest-22/8-puzzle-solver.git
cd 8-puzzle-solver


2️⃣ Install dependencies

Make sure you have Python 3.8+ installed. Then install Flask:

pip install flask

3️⃣ Run the app
python app.py

4️⃣ Open in browser

Go to:

http://127.0.0.1:5000/

📊 Algorithm Analysis
Algorithm	Completeness	Optimality	Time Complexity	Space Complexity
DFS	❌	❌	O(b^m)	O(bm)
IDS	✅	✅	O(b^d)	O(bd)
IDDFS	✅	✅	O(b^d)	O(bd)
A*	✅	✅	O(b^d)	O(b^d)

b: branching factor

d: depth of solution

m: maximum depth of search tree

📂 Project Structure
8-puzzle-solver/
│── static/          # CSS & JS files
│── templates/       # HTML files
│── app.py           # Flask backend
│── solver/          # Puzzle solver algorithms
│── README.md        # Project documentation

🙌 Acknowledgements

Inspired by Artificial Intelligence Search Algorithms in Computer Science.

Developed as part of a university AI project to explore search strategies.

📬 Contact

Ndivhadzo Ernest Singo

💼 inkedin.com/in/ernestsingo/

🌐 GitHub.com/Ernest-22

📧 ndivhadzosingo@gmail.com
