from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layers import invert, rainbow, black, lighten, green, red, blue
from layer_util import background
import colorsys

class LayerStore(ABC):

    def __init__(self) -> None:
        self.color = None

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """
    def __init__(self) -> None:
        self.color = None
        self.store = None
        self.spec = False
    
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.store == None:
            if self.spec == True:
                return(0,0,0)
            else:
                return (255,255,255)
        if self.spec == False:
            return self.store.apply(start,timestamp,x,y)
        elif self.spec == True:
            return invert.apply(self.store.apply(start,timestamp,x,y),0,0,0)
        
    
    def add(self, Layer):
        if self.store == Layer:
            return False
        self.store = Layer
        return True
    
    def erase(self, layer):
        self.store = None
        return True
    
    def special(self):
        
        if self.spec == False:
            self.spec = True
        else:
            self.spec = False
        
        

    

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """
    def __init__(self) -> None:
        self.color = None
        self.store = []
        self.spec = False
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if len(self.store) == 0:
            return start
        
        for i in range(len(self.store)):
            start = self.store[i].apply(start,timestamp,x,y)
        return start
        
    def add(self, layer):
        self.store.append(layer)
    
    def erase(self,layer):
        self.store.pop(0)
    
    def special(self):
        x = []
        for i in range(len(self.store)-1,-1,-1):
            x.append(self.store[i])
        self.store = x
        

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    pass


if __name__ == "__main__":
    s = SetLayerStore()
    # s.color = (100,100,100)
    s.add(lighten)
    s.add(rainbow)
    s.special()
    print(s.store)