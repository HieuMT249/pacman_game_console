import PacmanAgents
from search import Search
import argparse
import os
import time
from collections import OrderedDict

class Pacman: 
    
    # Hàm khởi tạo
    def __init__(self, map_file):
        self.map_data = self.load_map(map_file)
        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0])
        self.corners = [(1, 1), (1, self.cols - 2), (self.rows - 2, 1), (self.rows - 2, self.cols - 2)]
        
    # Hàm dùng để đọc map từ file
    def load_map(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        map_data = [list(line.strip()) for line in lines]
        
        return map_data
   
    # Hàm dùng để truyền map đọc được
    def map(self):
        return self.map_data
    
    # Hàm khởi chạy thuật toán
    def run_algorithm(self, algorithm_name, pacman_position, food_positions, map):
        food_corner_positions = list(OrderedDict.fromkeys(food_positions + self.corners))
        search_algorithm = Search(map)
        current_position = pacman_position
        total_cost = 0
        actions = []
        
        if algorithm_name == 'UCS': 
            while food_positions:
                for goal in food_corner_positions:
                    paths, cost = search_algorithm.ucs(current_position, [goal])
                    total_cost+=cost
                    # Cập nhật vị trí hiện tại
                    current_position = paths[0][-1] if paths else current_position
                    
                    # In từng bước trong mỗi path
                    for _, path in enumerate(paths):
                        actions.extend(self.get_actions(path))
                        for position in path:
                            self.visualize_game(position, food_positions)
            print('Actions:', actions)
            print('Total Cost: ', total_cost)
            
        
        elif algorithm_name == 'A*':
            while food_positions:
                for goal in food_corner_positions:
                    paths, cost = search_algorithm.a_star(current_position, [goal])
                    total_cost+=cost
                    # Cập nhật vị trí hiện tại
                    current_position = paths[0][-1] if paths else current_position
                    
                    # In từng bước trong mỗi path
                    for _, path in enumerate(paths):
                        actions.extend(self.get_actions(path))
                        for position in path:
                            self.visualize_game(position, food_positions)
            print('Actions:', actions)
            print('Total Cost: ', total_cost)
        else:
            raise ValueError("Unsupported algorithm")
    
    def get_actions(self, path):
        actions = []
        for i in range(1, len(path)):
            current_position = path[i - 1]
            next_position = path[i]
            action = self.get_action(current_position, next_position)
            actions.append(action)
        return actions

    def get_action(self, current_position, next_position):
        x = next_position[0] - current_position[0]
        y = next_position[1] - current_position[1]

        if x == 1:
            return 'South'
        elif x == -1:
            return 'North'
        elif y == 1:
            return 'East'
        elif y == -1:
            return 'West'
        else:
            return 'Stop'
    
    def draw_map(self, pacman_position, food_positions):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) == pacman_position:
                    print('P', end=' ')  # vị trí của Pacman
                elif (row, col) in food_positions:
                    print('.', end=' ')  # điểm mồi
                elif self.map_data[row][col] == '%':
                    print('%', end=' ')  # tường
                else:
                    print(' ', end=' ')
            print()  # Xuống dòng sau mỗi hàng

    # thêm chậm trễ giữa các bước
    def visualize_game(self, pacman_position, food_positions):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # loại bỏ điểm mồi nếu Pacman chạm vào
        if pacman_position in food_positions:
            food_positions.remove(pacman_position)
            
        self.draw_map(pacman_position, food_positions)
        time.sleep(0.2)    

def main():
    parser = argparse.ArgumentParser(description='Run Pacman game with specified map and algorithm.')
    parser.add_argument('--layout', type=str, required=True, help='Layout name (smallMaze, mediumMaze, bigMaze')
    parser.add_argument('--algorithm', type=str, choices=['UCS', 'A*'], default='UCS', help='Algorithm to use (UCS or A*)')
    
    args = parser.parse_args()
    
    # truyền dữ liệu map đọc được vào
    map_file = f'pacman_layouts/{args.layout}.lay'
    
    pacman_game = Pacman(map_file)
    
    # xác định các trạng thái của game (vị trí pacman, điểm mồi)
    game_state = PacmanAgents.create_game_state(pacman_game.map())
    
    pacman_game.run_algorithm(args.algorithm,game_state.pacman_position,game_state.food_positions,pacman_game.map())
    
if __name__ == "__main__":
    main()
