from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Node:
    id: int
    x: float
    y: float
    z: float = 0.0

@dataclass(frozen=True)
class Member:
    id: int
    start_node: int
    end_node: int
    area: float
    E: float

class StructuralModel:
    def __init__(self):
        self.nodes = {}
        self.members = {}
        self.loads = {}
        self.supports = {}

    def add_node(self, node_id, x, y, z=0.0):
        self.nodes[node_id] = Node(node_id, float(x), float(y), float(z))

    def add_member(self, member_id, start_node, end_node, area, E):
        if start_node not in self.nodes or end_node not in self.nodes:
            raise KeyError("Both member nodes must exist before adding a member.")
        self.members[member_id] = Member(member_id, start_node, end_node, float(area), float(E))

    def add_load(self, node_id, fx=0.0, fy=0.0):
        if node_id not in self.nodes:
            raise KeyError(f"Unknown node {node_id}")
        self.loads[node_id] = np.array([float(fx), float(fy)])

    def add_support(self, node_id, ux=False, uy=False):
        if node_id not in self.nodes:
            raise KeyError(f"Unknown node {node_id}")
        self.supports[node_id] = {"ux": bool(ux), "uy": bool(uy)}
