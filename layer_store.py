from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layers import invert, rainbow, black, lighten
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
    
    def checkSpec(self,x):
        if self.spec == True:
            return(255-x[0],255-x[1],255-x[2])
        else:
            return x
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        self.color = start
        
        if self.store == None:
            color = self.checkSpec(self.color)
            return color
                    
        elif self.store == black:
            initial = (0,0,0)
        
        elif self.store == invert:
            initial = tuple(255 - c for c in self.color)
        
        elif self.store == lighten:
            initial = tuple(min(255, x + 40) for x in self.color)
        
        elif self.store == rainbow:
            initial = tuple(
            int(255*x)
            for x in colorsys.hls_to_rgb((timestamp/20 + x/20 + y/20)%1, 0.6, 0.6)
        )
        
        color = self.checkSpec(initial)
        return color
    
    def add(self, Layer):
        if self.store == Layer:
            return False
        self.store = Layer
        return True
    
    def erase(self, layer):
        self.store = None
        return True
    
    def special(self):
        # print("special tapped")
        if self.spec == False:
            self.spec = True
            
        elif self.spec == True:
            self.spec = False
        # x = []
        # for i in self.color:
        #     x.append(255-i)
        # self.color = tuple(x)
        # return tuple(x)
            

    

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    pass

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