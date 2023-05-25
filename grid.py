from tile import Tile, TileState

from enum import Enum
from typing import Tuple, List
import random
from copy import deepcopy

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Grid():
    def __init__(self, width: int, height: int) -> None:
        if width*height < 30:
            raise Exception('Sorry! The minimum amount of squares is 30. Try specifying higher dimensions')
        self.width = width
        self.height = height
        self.player_x = 0
        self.player_y = 0
        self.board: List[List[Tile]] = []
        self.resetpoint: List[List[Tile]] = []
        # Fill the board with empty_char
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(Tile())

            self.board.append(row)

        # Initialize player
        self.board[0][0] = Tile(state=TileState.player)
        self.resetpoint = deepcopy(self.board)
        

    def print_board(self) -> None:
        for row in self.board:
            for col in row:
                print(col.face, end=' ')

            print()
    
    def set_player_position(self, x: int, y: int, direction: Direction) -> None:
        player_x, player_y = self.get_player_pos()
        if (x, y) == (player_x, player_y):
            return

        # error handling
        if x < 0 or y < 0:
            raise ValueError('X and Y cannot be below 0')
        if y > len(self.board) - 1 or x > len(self.board[0]) - 1:
            raise ValueError('Tried to place player out of bounds')
        
        if self.board[y][x].state == TileState.box:
            # Push the box
            self.move_box(x, y, direction)

        if self.board[y][x].state == TileState.goal:
            self.board[y][x] = Tile(state=TileState.player_on_goal)
        elif self.board[y][x].state == TileState.complete:
            self.board[y][x] = Tile(state=TileState.player_on_complete)
        else:
            self.board[y][x] = Tile(state=TileState.player)

        if self.board[player_y][player_x].state == TileState.player_on_goal:
            self.board[player_y][player_x] = Tile(state=TileState.goal)
        elif self.board[player_y][player_x].state == TileState.player_on_complete:
            self.board[player_y][player_x] = Tile(state=TileState.complete)
        else:
            self.board[player_y][player_x] = Tile(state=TileState.empty)

        self.player_x = x
        self.player_y = y

    def move_player_in_direction(self, direction: Direction) -> None:
        player_x, player_y = self.get_player_pos()
        # Perform the movement depending on the Enum
        match direction:
            case direction.UP:
                player_y -= 1
            case direction.DOWN:
                player_y += 1
            case direction.LEFT:
                player_x -= 1
            case direction.RIGHT:
                player_x += 1
        
        # Set player pos or return if out of bounds
        try:
            self.set_player_position(player_x, player_y, direction)
        except ValueError:
            return
        
    def move_box(self, box_x: int, box_y: int, direction: Direction) -> None:
        match direction:
            case direction.UP:
                box_y -= 1
            case direction.DOWN:
                box_y += 1
            case direction.LEFT:
                box_x -= 1
            case direction.RIGHT:
                box_x += 1
        
        if box_x < 0 or box_y < 0:
            raise ValueError('X and Y cannot be below 1')
        if box_y > len(self.board) - 1 or box_x > len(self.board[0]) - 1:
            raise ValueError('Tried to place box out of bounds')
        if self.board[box_y][box_x].state == TileState.box or self.board[box_y][box_x].state == TileState.complete:
            raise ValueError('Cannot move box into this tile')
        
        if self.board[box_y][box_x].state == TileState.goal:
            self.board[box_y][box_x] = Tile(state=TileState.complete)
            return

        self.board[box_y][box_x] = Tile(state=TileState.box)

    def get_player_pos(self) -> Tuple[int, int]:
        return (self.player_x, self.player_y)
    
    def spawn_box(self) -> None:
        row_idx = random.randrange(1, self.height - 1)
        col_idx = random.randrange(1, self.width - 1)

        player_pos = self.get_player_pos()

        if player_pos == (col_idx, row_idx) or self.board[row_idx][col_idx].state == TileState.box or self.board[row_idx][col_idx].state == TileState.goal:
            self.spawn_box()
            return
        
        self.board[row_idx][col_idx] = Tile(state=TileState.box)
        self.resetpoint[row_idx][col_idx] = Tile(state=TileState.box)

    def spawn_goal(self) -> None:
        row_idx = random.randrange(1, self.height - 1)
        col_idx = random.randrange(1, self.width - 1)

        player_pos = self.get_player_pos()

        if player_pos == (col_idx, row_idx) or self.board[row_idx][col_idx].state == TileState.goal or self.board[row_idx][col_idx].state == TileState.box:
            self.spawn_goal()
            return
        
        self.board[row_idx][col_idx] = Tile(state=TileState.goal)
        self.resetpoint[row_idx][col_idx] = Tile(state=TileState.goal)
    

    def check_completion(self) -> bool:
        flag = True
        for row in self.board:
            for col in row:
                if col.state == TileState.box:
                    flag = False
                    break

        return flag
    
    def reset(self):
        self.player_x = 0
        self.player_y = 0
        self.board = deepcopy(self.resetpoint)