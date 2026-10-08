import sys
sys.path.append("src")
import streamlit as st
from structural_toolkit.model import StructuralModel
from structural_toolkit.solver import TrussSolver
from structural_toolkit.results import print_results

st.set_page_config(page_title="Structural CAD-to-Analysis Toolkit",layout="wide")
st.title("Structural CAD-to-Analysis Toolkit")
st.caption("AutoCAD/DXF → Structural Model → Matrix Stiffness → Results → 3D/Mesh")

st.sidebar.header("Demo model")
E=st.sidebar.number_input("Young's modulus (GPa)",1.0,500.0,200.0)
A=st.sidebar.number_input("Area (mm²)",1.0,10000.0,2000.0)
P=st.sidebar.number_input("Vertical load (kN)",-1000.0,1000.0,-100.0)
if st.button("Run CE272-style truss"):
    m=StructuralModel(); Epa=E*1e9; Amp=A*1e-6
    for nid,x,y in [(1,0,0),(2,1,1),(3,1,0),(4,2,1)]: m.add_node(nid,x,y)
    for mid,a,b in [(1,1,2),(2,1,3),(3,2,3),(4,2,4),(5,3,4)]: m.add_member(mid,a,b,Amp,Epa)
    m.add_support(1,ux=True,uy=True); m.add_support(4,ux=True,uy=True)
    m.add_load(2,fy=P*1000); m.add_load(3,fx=40e3)
    s=TrussSolver(m); s.solve()
    st.subheader("Nodal displacements")
    st.dataframe({"Node":s.node_ids,"Ux (mm)":[s.U[s.dof_indices(n)[0]]*1000 for n in s.node_ids],"Uy (mm)":[s.U[s.dof_indices(n)[1]]*1000 for n in s.node_ids]})
    st.subheader("Member forces")
    st.dataframe({"Member":list(s.member_forces),"Force (kN)":[v/1000 for v in s.member_forces.values()]})
    st.success("Analysis completed.")
