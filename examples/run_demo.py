import sys
sys.path.append("src")
from examples.models.demo_truss import create_demo_truss
from structural_toolkit.solver import TrussSolver
from structural_toolkit.results import print_results
from structural_toolkit.export import export_member_forces,export_displacements
s=TrussSolver(create_demo_truss()); s.solve(); print_results(s)
export_member_forces(s,"validation/python_member_forces.csv"); export_displacements(s,"validation/python_displacements.csv")
