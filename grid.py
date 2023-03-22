from __future__ import annotations
from layer_store import LayerStore, SetLayerStore, AdditiveLayerStore, SequenceLayerStore
from data_structures.abstract_list import List
from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack
# from undo import UndoTracker
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
        # self.paint = ArrayStack(10000)
        # self.redo = ArrayStack(10000)
        self.grid = ArrayR(x)
        for i in range(x):
            sub = ArrayR(y)
            for j in range(y):
                if draw_style == self.DRAW_STYLE_SET:
                    sub[j] = SetLayerStore()
                if draw_style == self.DRAW_STYLE_ADD:
                    sub[j] = AdditiveLayerStore()
                if draw_style == self.DRAW_STYLE_SEQUENCE:
                    sub[j] = SequenceLayerStore()
            self.grid[i] = sub
              
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
        for i in range(self.x):
            for j in range(self.y):
                self.grid[i][j].special()
    
if __name__ == "__main__":
    g = Grid("set",5,6)
    print(g.grid[2][1])
    print(g.grid[2][3])
