from dataclasses import dataclass
@dataclass(frozen=True)
class Opening:
    x: float; y: float; width: float; height: float
class Wall:
    def __init__(self,width,height,thickness): self.width=width; self.height=height; self.thickness=thickness; self.openings=[]
    def add_opening(self,x,y,width,height): self.openings.append(Opening(x,y,width,height))
    @property
    def gross_area(self): return self.width*self.height
    @property
    def opening_area(self): return sum(o.width*o.height for o in self.openings)
    @property
    def net_area(self): return max(0.0,self.gross_area-self.opening_area)
    @property
    def volume(self): return self.net_area*self.thickness
