import sys
sys.path.append("src")
from structural_toolkit.model import StructuralModel

def create_demo_truss():
    m=StructuralModel(); E=200e9; A=2000e-6
    m.add_node(1,0,0); m.add_node(2,4,0); m.add_node(3,2,3)
    m.add_member(1,1,2,A,E); m.add_member(2,1,3,A,E); m.add_member(3,2,3,A,E)
    m.add_support(1,ux=True,uy=True); m.add_support(2,uy=True); m.add_load(3,fy=-100000)
    return m
