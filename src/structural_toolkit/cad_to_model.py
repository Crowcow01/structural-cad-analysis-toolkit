from structural_toolkit.model import StructuralModel


def coordinate_key(x, y, tolerance=1e-6):
    return (round(x / tolerance) * tolerance, round(y / tolerance) * tolerance)


def lines_to_model(lines, area, E):
    """Convert CAD line endpoints into a 2D truss model.

    Boundary conditions and loads are intentionally not inferred from arbitrary geometry.
    """
    model = StructuralModel()
    node_map = {}
    next_node_id = 1

    for line in lines:
        for x, y in [(line.x1, line.y1), (line.x2, line.y2)]:
            key = coordinate_key(x, y)
            if key not in node_map:
                node_map[key] = next_node_id
                model.add_node(next_node_id, x, y)
                next_node_id += 1

    member_id = 1
    for line in lines:
        a = node_map[coordinate_key(line.x1, line.y1)]
        b = node_map[coordinate_key(line.x2, line.y2)]
        if a != b:
            model.add_member(member_id, a, b, area, E)
            member_id += 1
    return model
