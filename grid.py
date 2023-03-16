from __future__ import annotations
from layer_store import LayerStore, SetLayerStore
from data_structures.abstract_list import List
class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        self.draw_style = draw_style
        self.brush_size = self.DEFAULT_BRUSH_SIZE
        self.x = x
        self.y = y
        self.grid = []
        for i in range(x+1):
            sub = []
            for j in range(y+1):
                sub.append(SetLayerStore())
            self.grid.append(sub)
              
    def __getitem__(self, key):
        return self.grid[key]    

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size >= self.MAX_BRUSH:
            return False
        self.brush_size += 1
        print(f"bruh size is now {self.brush_size}")
        

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size <= self.MIN_BRUSH:
            return False
        self.brush_size -= 1
        print(f"bruh size is now {self.brush_size}")

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        raise NotImplementedError()
    
if __name__ == "__main__":
    g = Grid("set",5,6)
    print(g.grid)
