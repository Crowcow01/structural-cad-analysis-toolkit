def print_results(solver):
    print("\n"+"="*68); print("STRUCTURAL ANALYSIS RESULTS"); print("="*68)
    print("\nNODAL DISPLACEMENTS (mm)")
    for nid in solver.node_ids:
        ux,uy=solver.dof_indices(nid); print(f"Node {nid:>3}: Ux={solver.U[ux]*1000:>12.6f}  Uy={solver.U[uy]*1000:>12.6f}")
    print("\nMEMBER AXIAL FORCES (kN)")
    for mid,f in solver.member_forces.items():
        state="TENSION" if f>1e-9 else "COMPRESSION" if f<-1e-9 else "ZERO"
        print(f"Member {mid:>3}: {f/1000:>12.6f}  {state}")
    print("\nSUPPORT REACTIONS (kN)")
    for nid in solver.model.supports:
        rx,ry=solver.dof_indices(nid); print(f"Node {nid:>3}: Rx={solver.R[rx]/1000:>12.6f}  Ry={solver.R[ry]/1000:>12.6f}")
    print("="*68)
