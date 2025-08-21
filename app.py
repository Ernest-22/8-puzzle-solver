from flask import Flask, render_template, request, jsonify
from queue import PriorityQueue
import copy
import time
import random
import sys
sys.setrecursionlimit(12000)  # Increase if needed


app = Flask(__name__)

# Goal state for the 8-puzzle
GOAL_STATE = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]  # The empty space is represented by 0

# Directions for moving the blank tile (row, col)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

# Find the position of the blank tile
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

# Check if the puzzle state matches the goal
def is_goal(state):
    return state == GOAL_STATE

# Get the neighbors of the current state by moving the blank tile
def get_neighbors(state):
    neighbors = []
    row, col = find_blank(state)

    for dr, dc in DIRECTIONS:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = copy.deepcopy(state)
            new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
            neighbors.append(new_state)

    return neighbors

# Convert state to a tuple for use in sets (to track explored nodes)
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

# Breadth-Limited Search (BLS)
def breadth_limited_search(state, limit, path, explored):
    if is_goal(state):
        return path + [state]

    explored.add(state_to_tuple(state))
    neighbors = get_neighbors(state)

    for i, neighbor in enumerate(neighbors):
        if i >= limit:
            break
        if state_to_tuple(neighbor) not in explored:
            result = breadth_limited_search(neighbor, limit, path + [state], explored)
            if result is not None:
                return result

    return None

# Iterative Breadth Search (IBS)
def ibs_solver(initial_state):
    for breadth in range(1, 31):
        explored = set()
        result = breadth_limited_search(initial_state, breadth, [], explored)
        if result is not None:
            return result, len(explored)
    return "No solution found.", 0

# Depth-First Search (DFS)
def dfs_solver(initial_state, max_depth=20):
    stack = [(initial_state, [], 0)]
    explored = set()
    nodes_expanded = 0

    while stack:
        state, path, depth = stack.pop()

        if is_goal(state):
            return path + [state], nodes_expanded
        
        state_tuple = state_to_tuple(state)
        if state_tuple in explored or depth > max_depth:
            continue
        
        explored.add(state_tuple)
        nodes_expanded += 1

        for neighbor in get_neighbors(state):
            if state_to_tuple(neighbor) not in explored:
                stack.append((neighbor, path + [state], depth + 1))

    return "No solution found.", nodes_expanded

# Heuristic: Misplaced Tiles
def misplaced_tiles(state):
    misplaced = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != GOAL_STATE[i][j]:
                misplaced += 1
    return misplaced

# A* Search with Misplaced Tiles heuristic
def astar_solver(initial_state):
    frontier = PriorityQueue()
    frontier.put((misplaced_tiles(initial_state), 0, initial_state, []))
    explored = set()
    nodes_expanded = 0

    while not frontier.empty():
        priority, moves, state, path = frontier.get()
        if is_goal(state):
            return path + [state], nodes_expanded
        state_tuple = state_to_tuple(state)
        if state_tuple in explored:
            continue
        explored.add(state_tuple)
        nodes_expanded += 1

        for neighbor in get_neighbors(state):
            neighbor_tuple = state_to_tuple(neighbor)
            if neighbor_tuple not in explored:
                new_moves = moves + 1
                new_priority = new_moves + misplaced_tiles(neighbor)
                frontier.put((new_priority, new_moves, neighbor, path + [state]))

    return "No solution found.", nodes_expanded

# Iterative Deepening Depth-First Search (IDDFS)
def iddfs_solver(initial_state):
    def dls(state, limit, explored):
        if is_goal(state):
            return [state]
        if limit == 0:
            return None
        explored.add(state_to_tuple(state))
        for neighbor in get_neighbors(state):
            if state_to_tuple(neighbor) not in explored:
                result = dls(neighbor, limit - 1, explored)
                if result:
                    return [state] + result
        return None

    for depth in range(1, 31):
        explored = set()
        result = dls(initial_state, depth, explored)
        if result:
            return result, len(explored)
    return "No solution found.", 0

# Check if the puzzle is solvable
def is_solvable(state):
    flat_state = [num for row in state for num in row if num != 0]
    inversions = 0

    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:
                inversions += 1

    return inversions % 2 == 0

# Shuffle the puzzle
def shuffle_state(state):
    for _ in range(100):
        neighbors = get_neighbors(state)
        if neighbors:
            state = random.choice(neighbors)
    return state

# Route: Home page
@app.route('/')
def index():
    return render_template('index.html')

solution_path = []
# Route: Solve the puzzle
@app.route('/solve/<algorithm>', methods=['POST'])  # Updated to accept algorithm
def solve(algorithm):  # Accept algorithm as a parameter
    try:
        data = request.json
    
        initial_state = data.get('initial_state')

        # Log input data
        print(f"Received request for algorithm: {algorithm}, initial state: {initial_state}")

        # Validate initial state
        if not isinstance(initial_state, list) or len(initial_state) != 3 or any(len(row) != 3 for row in initial_state):
            print("Invalid initial state")
            return jsonify({"error": "Invalid initial state."}), 400

        # Check if puzzle is solvable
        if not is_solvable(initial_state):
            print("Puzzle configuration is not solvable.")
            return jsonify({"error": "The puzzle configuration is not solvable."}), 400

        # Timer to track performance
        start_time = time.time()

        # Select algorithm based on user input
        if algorithm == 'ibs':
            solution, nodes_expanded = ibs_solver(initial_state)
        elif algorithm == 'dfs':
            solution, nodes_expanded = dfs_solver(initial_state)
        elif algorithm == 'astar':
            solution, nodes_expanded = astar_solver(initial_state)
        elif algorithm == 'iddfs':
            solution, nodes_expanded = iddfs_solver(initial_state)
        else:
            print("Unknown algorithm requested.")
            return jsonify({"error": "Unknown algorithm."}), 400

        # Calculate time taken
        end_time = time.time()
        time_taken = (end_time - start_time) * 1000  # Convert to milliseconds

        # Log results
        print(f"Solution: {solution}, Nodes Expanded: {nodes_expanded}, Time Taken: {time_taken} ms")

        if solution == "No solution found.":
            print("No solution was found for the given state.")
            return jsonify({"error": "No solution found."}), 400



        return jsonify({
            "solution": solution,
            "time_taken": time_taken,
            "nodes_expanded": nodes_expanded,
            "solution_length": len(solution),
        }), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/next_step', methods=['GET'])
def next_step():
    global currentStep
    if currentStep < len(solution_path):
        next_state = solution_path[currentStep]
        currentStep += 1
        return jsonify(next_state), 200
    else:
        return jsonify({"error": "No more steps."}), 400


# Route: Shuffle the puzzle
@app.route('/shuffle', methods=['POST'])
def shuffle():
    initial_state = request.json.get('initial_state', [])
    shuffled_state = shuffle_state(initial_state)
    return jsonify({"shuffled_state": shuffled_state}), 200

@app.route('/compare', methods=['POST'])
@app.route('/compare', methods=['POST'])
def compare_algorithms():
    try:
        # Get the initial state from the request
        data = request.json
        initial_state = data.get('initial_state')

        if not isinstance(initial_state, list) or len(initial_state) != 3 or any(len(row) != 3 for row in initial_state):
            return jsonify({"error": "Invalid initial state."}), 400

        # Check if the puzzle is solvable
        if not is_solvable(initial_state):
            return jsonify({"error": "The puzzle configuration is not solvable."}), 400

        # Dictionary to store the results for each algorithm
        results = {}
        algorithms = ['ibs', 'dfs', 'astar', 'iddfs']

        # Solve the puzzle using each algorithm and record the time taken
        for algorithm in algorithms:
            start_time = time.time()

            if algorithm == 'ibs':
                solution, nodes_expanded = ibs_solver(initial_state)
            elif algorithm == 'dfs':
                solution, nodes_expanded = dfs_solver(initial_state)
            elif algorithm == 'astar':
                solution, nodes_expanded = astar_solver(initial_state)
            elif algorithm == 'iddfs':
                solution, nodes_expanded = iddfs_solver(initial_state)

            end_time = time.time()
            time_taken = (end_time - start_time) * 1000  # Convert to milliseconds

            # Store the result
            results[algorithm] = {
                "time_taken": time_taken,
                "nodes_expanded": nodes_expanded,
                "solution_length": len(solution) if solution != "No solution found." else 0,
            }

        # Find the fastest algorithm
        fastest_algorithm = min(results, key=lambda k: results[k]['time_taken'])
        fastest_time = results[fastest_algorithm]['time_taken']

        return jsonify({
            'results': results,
            'fastest_algorithm': fastest_algorithm,
            'fastest_time': fastest_time
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
