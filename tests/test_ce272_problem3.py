import sys
sys.path.append("src")
from examples.ce272_problem3 import create_problem3
from structural_toolkit.solver import TrussSolver

def test_ce272_problem3():
    s=TrussSolver(create_problem3()); s.solve()
    u2=s.U[s.dof_indices(2)[0]]*1000; v3=s.U[s.dof_indices(3)[1]]*1000; f23=s.member_forces[3]/1000
    assert abs(u2-0.150)<0.005
    assert abs(v3-(-0.475))<0.01
    assert abs(f23-(-40.0))<0.5
