import sys
sys.path.append("src")
from structural_toolkit.model import StructuralModel
from structural_toolkit.solver import TrussSolver
from structural_toolkit.results import print_results
from structural_toolkit.benchmark import print_benchmark

def create_problem3():
    m=StructuralModel(); E=200e9; A=2000e-6
    for nid,x,y in [(1,0,0),(2,1,1),(3,1,0),(4,2,1)]: m.add_node(nid,x,y)
    for mid,a,b in [(1,1,2),(2,1,3),(3,2,3),(4,2,4),(5,3,4)]: m.add_member(mid,a,b,A,E)
    m.add_support(1,ux=True,uy=True); m.add_support(4,ux=True,uy=True)
    m.add_load(2,fy=-100000); m.add_load(3,fx=40000)
    return m
if __name__ == "__main__":
    s=TrussSolver(create_problem3()); s.solve(); print_results(s)
    print("\nCE272 benchmark")
    print_benchmark("u2",s.U[s.dof_indices(2)[0]]*1000,0.150,"mm")
    print_benchmark("v3",s.U[s.dof_indices(3)[1]]*1000,-0.475,"mm")
    print_benchmark("F23",s.member_forces[3]/1000,-40.0,"kN")
