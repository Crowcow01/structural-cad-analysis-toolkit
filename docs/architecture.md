# Technical Architecture

## Layer 1 — Geometry
`dxf_reader.py` converts AutoCAD DXF LINE entities into a neutral `CADLine` representation.

## Layer 2 — Structural model
`cad_to_model.py` converts CAD endpoints into unique nodes and CAD lines into members. The structural model stores nodes, members, supports and loads independently of the CAD format.

## Layer 3 — Analysis
`solver.py` assembles the global stiffness matrix and solves the free degrees of freedom. Reactions are recovered from `R = KU - F`. Member axial forces are recovered from axial extension.

## Layer 4 — Results
`results.py` formats human-readable results and `export.py` writes machine-readable CSV files.

## Layer 5 — Validation
The CE272 benchmark provides a regression test. SAP2000 tables are treated as an external reference dataset and compared through `validation.py`.

## Layer 6 — Wall/mesh pipeline
`wall.py` defines parametric wall geometry and openings. `mesh.py` sends the resulting geometry to Gmsh for surface meshing.
