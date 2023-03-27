from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.bset import BSet
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import *
from layers import invert, rainbow, black, lighten, green, red, blue, sparkle, darken
from layer_util import *
import colorsys

class LayerStore(ABC):
    
    NUMBER_OF_LAYERS = len(get_layers())

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
        self.store = None
        self.spec = False
    
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        if self.store == None:
            if self.spec == True:
                return invert.apply(start,timestamp,x,y)
            else:
                return start
            
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
        self.store = CircularQueue(100)
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        color = start     
           
        for i in range(len(self.store)):
            next_layer = self.store.serve()
            self.store.append(next_layer)
            color = next_layer.apply(color,timestamp,x,y)
        return color
        
    def add(self, layer):
        self.store.append(layer)
        return True
    
    def erase(self,layer):
        if self.store.is_empty() == True:
            return False
        self.store.serve()
        return True
        
    
    def special(self):
        s1 = ArrayStack(len(self.store))
        
        for i in range(len(self.store)):
            l1 = self.store.serve()
            s1.push(l1)
        
        q1 = CircularQueue(len(s1))
        
        for i in range(len(s1)):
            l2 = s1.pop()
            q1.append(l2)
            
        self.store = q1
        

class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """
    def __init__(self) -> None:
        self.store = BSet()
        self.layers = get_layers()       
    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        color = start
        for i in range(1,self.NUMBER_OF_LAYERS):
            if i in self.store:
                color = self.layers[i-1].apply(color, timestamp, x, y)     
                    
        return color
    
    def add(self, layer):
        layer_index = layer.index+1
        self.store.add(layer_index)
        return True
        
        
    def erase(self,layer):
        layer_index = layer.index+1
        if (layer_index) not in self.store:
            return False
        self.store.remove(layer_index)
        return True
    
    def special(self):
        
        if self.store.is_empty():
            return False
        
        lst = ArraySortedList(9)
        for i in range(1,self.NUMBER_OF_LAYERS):
            if i in self.store:
                a = ListItem(self.layers[i-1],self.layers[i-1].name)
                lst.add(a)
        
        middle = len(lst)//2
        if len(lst) % 2 == 0:
            middle = (len(lst)//2) -1
        deleted_item = lst.delete_at_index(middle).value

        self.erase(deleted_item)     
                

if __name__ == "__main__":
    
    s = SequenceLayerStore()
    s.add(invert)
    s.add(lighten)
    s.add(rainbow)
    s.add(black)
    print(s.get_color((100, 100, 100), 0, 0, 0)) #(215, 215, 215)
    s.special() # Ordering: Black, Invert, Lighten, Rainbow.
                # Remove: Invert
    print(s.get_color((100, 100, 100), 7, 0, 0)) #(40, 40, 40)
    s.special() # Ordering: Black, Lighten, Rainbow.
                # Remove: Lighten
    print(s.get_color((100, 100, 100), 7, 0, 0)) #(0, 0, 0)
    s.special() # Ordering: Black, Rainbow.
                # Remove: Black
    print(s.get_color((100, 100, 100), 7, 0, 0)) #(91, 214, 104)
    