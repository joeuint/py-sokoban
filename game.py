from grid import Grid, Direction
import os

controls = {
    'right': ['right', 'd'],
    'left': ['left', 'a'],
    'up': ['up', 'w'],
    'down': ['down', 's'],
    'reset': ['reset', 'r'],
    'regen': ['regen'],
    'exit': ['exit']
}

def spawn_objective(grid: Grid, count: int):
    for _ in range(0, count):
        grid.spawn_box()
        grid.spawn_goal()

def main():
    level = 1

    while True:
        grid = Grid(10, 10)
        spawn_objective(grid, level)
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Level', level)
            grid.print_board()
            if grid.check_completion():
                break
            key = input('Key: ').lower()
            match key:
                case w if w in controls.get('right'):
                    grid.move_player_in_direction(Direction.RIGHT)
                case w if w in controls.get('left'):
                    grid.move_player_in_direction(Direction.LEFT)
                case w if w in controls.get('up'):
                    grid.move_player_in_direction(Direction.UP)
                case w if w in controls.get('down'):
                    grid.move_player_in_direction(Direction.DOWN)
                case w if w in controls.get('reset'):
                    grid.reset()
                case w if w in controls.get('regen'):
                    level -= 1
                    break
                case w if w in controls.get('exit'):
                    exit()
        
        level += 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()