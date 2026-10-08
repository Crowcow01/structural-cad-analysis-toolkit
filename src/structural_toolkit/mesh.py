from pathlib import Path
import gmsh


def _finish(filename):
    gmsh.model.mesh.generate(2)
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    gmsh.write(filename)
    return gmsh.model.mesh.getNodes(), gmsh.model.mesh.getElements()


def create_rectangle_mesh(width, height, mesh_size=0.25, filename="validation/wall.msh"):
    """Generate a 2D triangular mesh for a rectangular wall face."""
    gmsh.initialize()
    gmsh.model.add("wall")
    try:
        p = [gmsh.model.geo.addPoint(x, y, 0, mesh_size)
             for x, y in [(0, 0), (width, 0), (width, height), (0, height)]]
        lines = [gmsh.model.geo.addLine(p[i], p[(i + 1) % 4]) for i in range(4)]
        loop = gmsh.model.geo.addCurveLoop(lines)
        gmsh.model.geo.addPlaneSurface([loop])
        gmsh.model.geo.synchronize()
        return _finish(filename)
    finally:
        gmsh.finalize()


def create_wall_with_openings_mesh(wall, mesh_size=0.25,
                                   filename="validation/wall_openings.msh"):
    """Generate a 2D triangular wall-face mesh with rectangular openings removed."""
    gmsh.initialize()
    gmsh.model.add("wall_openings")
    try:
        outer = [gmsh.model.geo.addPoint(x, y, 0, mesh_size)
                 for x, y in [(0, 0), (wall.width, 0),
                              (wall.width, wall.height), (0, wall.height)]]
        outer_lines = [gmsh.model.geo.addLine(outer[i], outer[(i + 1) % 4]) for i in range(4)]
        loops = [gmsh.model.geo.addCurveLoop(outer_lines)]
        for o in wall.openings:
            pts = [gmsh.model.geo.addPoint(x, y, 0, mesh_size)
                   for x, y in [(o.x, o.y), (o.x + o.width, o.y),
                                (o.x + o.width, o.y + o.height),
                                (o.x, o.y + o.height)]]
            lines = [gmsh.model.geo.addLine(pts[i], pts[(i + 1) % 4]) for i in range(4)]
            loops.append(gmsh.model.geo.addCurveLoop(lines))
        gmsh.model.geo.addPlaneSurface(loops)
        gmsh.model.geo.synchronize()
        return _finish(filename)
    finally:
        gmsh.finalize()


def create_3d_wall_mesh(wall, mesh_size=0.25,
                        filename="validation/wall_3d.msh"):
    """Generate a tetrahedral 3D wall mesh by cutting openings through a wall solid."""
    gmsh.initialize()
    gmsh.model.add("wall_3d")
    try:
        outer = gmsh.model.occ.addBox(0, 0, 0, wall.width, wall.height, wall.thickness)
        tools = []
        eps = max(wall.thickness * 0.1, 1e-6)
        for o in wall.openings:
            tools.append(gmsh.model.occ.addBox(
                o.x, o.y, -eps, o.width, o.height, wall.thickness + 2 * eps
            ))
        if tools:
            cut, _ = gmsh.model.occ.cut([(3, outer)], [(3, tag) for tag in tools])
            volumes = cut
        else:
            volumes = [(3, outer)]

        gmsh.model.occ.synchronize()
        for dim, tag in volumes:
            gmsh.model.mesh.setSize(gmsh.model.getBoundary([(dim, tag)], True, False), mesh_size)
        gmsh.model.mesh.generate(3)
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        gmsh.write(filename)
        return gmsh.model.mesh.getNodes(), gmsh.model.mesh.getElements()
    finally:
        gmsh.finalize()
