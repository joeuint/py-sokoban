from enum import Enum

ZERO_WIDTH_CHAR = '​' # This is a zero width character (U+200b). Do not delete or else everything will break. If you remove it simply add the unicode glypg (U+200b)

class TileState(Enum):
    player = '♜'
    box = '☒'
    empty = '☐'
    goal = '⬤'
    complete = '★'
    player_on_goal = '♜' + ZERO_WIDTH_CHAR
    player_on_complete = '♜' + ZERO_WIDTH_CHAR + ZERO_WIDTH_CHAR

class Tile():
    def __init__(self, state: TileState=TileState.empty):
        self.state = state
        self.face = state.value