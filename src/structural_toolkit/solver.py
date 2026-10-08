import numpy as np

class TrussSolver:
    """2D pin-jointed truss solver using the direct stiffness method."""
    def __init__(self, model):
        self.model = model
        self.node_ids = sorted(model.nodes)
        self.node_index = {nid: i for i, nid in enumerate(self.node_ids)}
        self.ndof = 2 * len(self.node_ids)
        self.K = np.zeros((self.ndof, self.ndof))
        self.F = np.zeros(self.ndof)
        self.U = np.zeros(self.ndof)
        self.R = np.zeros(self.ndof)
        self.member_forces = {}

    def dof_indices(self, node_id):
        i = self.node_index[node_id]
        return [2*i, 2*i+1]

    def assemble_stiffness(self):
        for m in self.model.members.values():
            ni, nj = self.model.nodes[m.start_node], self.model.nodes[m.end_node]
            dx, dy = nj.x-ni.x, nj.y-ni.y
            L = float(np.hypot(dx, dy))
            if L <= 0: raise ValueError(f"Member {m.id} has zero length")
            c, s = dx/L, dy/L
            k = m.area*m.E/L
            ke = k*np.array([[c*c,c*s,-c*c,-c*s],[c*s,s*s,-c*s,-s*s],[-c*c,-c*s,c*c,c*s],[-c*s,-s*s,c*s,s*s]])
            dofs = self.dof_indices(m.start_node)+self.dof_indices(m.end_node)
            self.K[np.ix_(dofs,dofs)] += ke

    def assemble_load_vector(self):
        for nid, load in self.model.loads.items():
            self.F[self.dof_indices(nid)] += load

    def get_restrained_dofs(self):
        out=[]
        for nid,s in self.model.supports.items():
            ux,uy=self.dof_indices(nid)
            if s["ux"]: out.append(ux)
            if s["uy"]: out.append(uy)
        return sorted(set(out))

    def solve(self):
        self.assemble_stiffness(); self.assemble_load_vector()
        restrained=self.get_restrained_dofs()
        free=np.setdiff1d(np.arange(self.ndof), restrained)
        Kff=self.K[np.ix_(free,free)]
        if np.linalg.matrix_rank(Kff) < len(free):
            raise np.linalg.LinAlgError("Structure is unstable or insufficiently restrained.")
        self.U[free]=np.linalg.solve(Kff,self.F[free])
        self.R=self.K@self.U-self.F
        self.calculate_member_forces()
        return self.U

    def calculate_member_forces(self):
        for m in self.model.members.values():
            ni,nj=self.model.nodes[m.start_node],self.model.nodes[m.end_node]
            dx,dy=nj.x-ni.x,nj.y-ni.y; L=np.hypot(dx,dy); c,s=dx/L,dy/L
            u=self.U[self.dof_indices(m.start_node)+self.dof_indices(m.end_node)]
            extension=np.dot([-c,-s,c,s],u)
            self.member_forces[m.id]=m.area*m.E/L*extension
