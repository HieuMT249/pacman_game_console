class PacmanAgents:
    def __init__(self, pacman_position, food_positions, map_state):
        self.pacman_position = pacman_position
        self.food_positions = food_positions
        self.map_state = map_state
    
# Hàm tạo trạng thái từ bản đồ
def create_game_state(map_state):
    pacman_position = None
    food_positions = []

    for i, row in enumerate(map_state):
        for j, cell in enumerate(row):
            if cell == 'P':
                pacman_position = (i, j)
            elif cell == '.':
                food_positions.append((i, j))

    return PacmanAgents(pacman_position, food_positions, map_state)