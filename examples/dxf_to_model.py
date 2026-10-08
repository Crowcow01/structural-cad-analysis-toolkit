import sys
sys.path.append("src")
from structural_toolkit.dxf_reader import read_lines
from structural_toolkit.cad_to_model import lines_to_model
from structural_toolkit.solver import TrussSolver
lines=read_lines("cad/truss/truss.dxf",layer="STRUCTURAL_MEMBERS")
model=lines_to_model(lines,2000e-6,200e9)
print(f"Imported {len(model.nodes)} nodes and {len(model.members)} members")
# CAD geometry alone does not define supports/loads; these are intentionally explicit.
