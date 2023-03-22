from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:
    
    def __init__(self) -> None:
        self.paint = ArrayStack(10000)
        self.repaint = ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if self.paint.is_full():
            return None
        self.paint.push(action)
        
    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
        """
        if self.paint.is_empty():
            return None
        layer_undo = self.paint.pop()
        self.repaint.push(layer_undo)
        layer_undo.undo_apply(grid)
        return layer_undo
        

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """
        if self.repaint.is_empty():
            return None
        layer_redo = self.repaint.pop()
        self.paint.push(layer_redo)
        layer_redo.redo_apply(grid)
        return layer_redo
