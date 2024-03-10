# thuật toán sử dụng để giải bài toán (UCS or A*)

import heapq

class Search:
    
    def __init__(self, map):
        self.map_data = map
        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0])
        
    # Hàm kiểm tra xem đi có đúng hay không
    def is_valid_move(self, x, y):
            return 0 <= x < self.rows and 0 <= y < self.cols and self.map_data[x][y] != '%'
    
    def get_neighbors(self, x, y):
        neighbors = []
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
        for move in moves:
            new_x, new_y = x + move[0], y + move[1]
            if self.is_valid_move(new_x, new_y):
                neighbors.append((new_x, new_y))
        return neighbors
    # Thuật toán UCS
    def ucs(self, start, goals):
        paths = []
        total_cost = 0

        for goal in goals:
            priority_queue = [(0, start, [])]  # (cost, current_position, path_so_far)
            visited = set()

            while priority_queue:
                current_cost, current_position, path_so_far = heapq.heappop(priority_queue)

                if current_position == goal:
                    paths.append(path_so_far)
                    total_cost += current_cost
                    break

                if current_position in visited:
                    continue

                visited.add(current_position)

                for neighbor in self.get_neighbors(*current_position):
                    new_cost = current_cost + 1
                    heapq.heappush(priority_queue, (new_cost, neighbor, path_so_far + [neighbor]))
                    
        return paths, total_cost
    
    def a_star(self):
        return None