from structural_toolkit.wall import Wall
from structural_toolkit.mesh import create_3d_wall_mesh

wall = Wall(4.0, 3.0, 0.23)
wall.add_opening(0.8, 0.8, 1.2, 1.4)
wall.add_opening(2.6, 0.6, 0.8, 1.0)

nodes, elements = create_3d_wall_mesh(wall, mesh_size=0.25)
print("3D wall mesh generated:", len(nodes[0]), "node tags")
