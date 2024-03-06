import PacmanAgents
from search import Search
import argparse
import heapq
import os
import time

class Pacman: 
    
    # Hàm khởi tạo
    def __init__(self, map_file):
        self.map_data = self.load_map(map_file)
        self.rows = len(self.map_data)
        self.cols = len(self.map_data[0])
        
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
    def run_algorithm(self, algorithm_name, pacman_position, food_position, map):
        search_algorithm = Search(pacman_position, food_position, map)
        if algorithm_name == 'UCS':
            return search_algorithm.ucs(pacman_position, food_position)
        elif algorithm_name == 'A*':
            return search_algorithm.a_star()
        else:
            raise ValueError("Unsupported algorithm")
    
    
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
        time.sleep(1)

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
    
    # trả về đường đi và cost 
    paths, total_cost = pacman_game.run_algorithm(args.algorithm, game_state.pacman_position, game_state.food_positions, pacman_game.map())
    

    # In từng bước trong mỗi path
    for step, path in enumerate(paths):
        print(f"\nStep {step + 1}:")
        for position in path:
            pacman_game.visualize_game(position, game_state.food_positions)

    print('Paths: ', paths)
    print('Total Cost: ', total_cost)
    

if __name__ == "__main__":
    main()
