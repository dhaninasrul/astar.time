import heapq
import time
import random

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def generate_grid(total_nodes, num_obstacles):
    size = int(total_nodes ** 0.5)
    grid = [[0 for _ in range(size)] for _ in range(size)]

    obstacle_count = 0
    while obstacle_count < num_obstacles:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if (x, y) not in [(0, 0), (size - 1, size - 1)] and grid[x][y] == 0:
            grid[x][y] = 1
            obstacle_count += 1

    return grid, (0, 0), (size - 1, size - 1)

def get_neighbors(pos, grid):
    x, y = pos
    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
            neighbors.append((nx, ny))
    return neighbors

def astar(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (manhattan(start, goal), 0, start))
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, cost, current = heapq.heappop(open_set)
        if current == goal:
            return True
        if current in visited:
            continue
        visited.add(current)
        for neighbor in get_neighbors(current, grid):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                f = tentative_g + manhattan(neighbor, goal)
                heapq.heappush(open_set, (f, tentative_g, neighbor))
    return False

def run_astar_experiments():
    experiments = [
        (5000, 10),
        (50000, 100),
        (500000, 1000),
        (5000000, 10000),
        (50000000, 100000)
    ]
    results = []

    for nodes, obstacles in experiments:
        grid, start, goal = generate_grid(nodes, obstacles)

        start_time = time.time()
        astar(grid, start, goal)
        astar_time = (time.time() - start_time) * 1000

        results.append((nodes, obstacles, astar_time))
        print(f"[A*]   #node: {nodes} #obstacle: {obstacles} | Time: {astar_time:.2f} ms")

    return results

if __name__ == "__main__":
    run_astar_experiments()
