import csv

def export_member_forces(solver, filename):
    with open(filename,"w",newline="") as f:
        w=csv.writer(f); w.writerow(["member_id","force_N","force_kN","state"])
        for mid,force in solver.member_forces.items():
            state="TENSION" if force>1e-9 else "COMPRESSION" if force<-1e-9 else "ZERO"
            w.writerow([mid,force,force/1000,state])

def export_displacements(solver, filename):
    with open(filename,"w",newline="") as f:
        w=csv.writer(f); w.writerow(["node_id","Ux_m","Uy_m","Ux_mm","Uy_mm"])
        for nid in solver.node_ids:
            ux,uy=solver.dof_indices(nid); a,b=solver.U[ux],solver.U[uy]
            w.writerow([nid,a,b,a*1000,b*1000])
