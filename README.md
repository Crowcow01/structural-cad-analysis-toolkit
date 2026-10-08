# Structural CAD-to-Analysis Toolkit

**Python • AutoCAD/DXF • Structural Analysis • 3D Modelling • Mesh Generation • SAP2000 Validation**

A portfolio project designed around a practical structural-engineering workflow: convert CAD geometry into a computational structural model, analyse it with a matrix-stiffness solver, visualize the model/results, and generate wall meshes for downstream analysis.

## Why this project

The toolkit targets the same class of workflow used in structural-analysis software: geometry import, model creation, analysis, visualization, wall/opening modelling, and mesh generation. It is intentionally modular so that each stage can be tested independently.

## Architecture

```text
AutoCAD
   │
   └── DXF
        │
        ▼
 CAD/DXF Parser ──► Structural Model
                         │
                         ▼
                 Matrix-Stiffness Solver
                    │      │      │
                    ▼      ▼      ▼
               Displacements Forces Reactions
                    │
                    ▼
                 Visualization

Wall Geometry ──► Openings ──► Net Area ──► Gmsh Mesh

SAP2000 benchmark ───────────────► Validation / Error report
```

## Features

- 2D truss structural model with nodes, members, supports and loads.
- Direct matrix-stiffness solution using NumPy.
- Nodal displacements, member axial forces and support reactions.
- CE272 Matrix Displacement Method benchmark for Problem 3.
- AutoCAD/DXF LINE import using `ezdxf`.
- Automatic node deduplication from CAD line endpoints.
- Parametric wall model with rectangular openings and net area/volume calculation.
- 3D wall geometry helpers.
- Gmsh-based triangular surface mesh generation, including openings.
- Plotly 3D structural visualization.
- Streamlit demonstration UI.
- SAP2000 validation layer based on exported tables.
- Pytest regression tests.

## Quick start

```bash
python -m venv .venv
.venv\\Scripts\\activate          # Windows
pip install -r requirements.txt
```

Run the CE272 benchmark:

```bash
python examples/ce272_problem3.py
```

Run tests:

```bash
pytest
```

Run the application:

```bash
streamlit run app/streamlit_app.py
```

## CE272 benchmark

The repository uses the published CE272 Problem 3 reference values as a regression benchmark: `u2 = 0.150 mm`, `v3 = -0.475 mm`, and `F23 = -40 kN`. The implementation reproduces these values within engineering tolerance rather than hard-coding the answers.

## AutoCAD workflow

Create/export a DXF with structural member lines on the `STRUCTURAL_MEMBERS` layer. The importer reads LINE entities and converts unique endpoints into nodes.

```bash
python examples/dxf_to_model.py
```

The current importer deliberately does **not** guess supports or loads from arbitrary CAD geometry. Those boundary conditions must be explicitly defined until a controlled layer/block convention is implemented.

Recommended CAD layers for the next interface version:

- `STRUCTURAL_MEMBERS`
- `NODES`
- `SUPPORTS`
- `LOADS`
- `WALLS`
- `OPENINGS`

## SAP2000 validation

SAP2000 is used as an **external validation benchmark**, not as a claim that this project reproduces SAP2000 internally.

Export the relevant SAP2000 tables and place normalized CSV files in `validation/sap2000/`. The intended schema is documented there. Then use `structural_toolkit.validation.compare_results()` to produce member/node error tables.

The source CE272 assignment explicitly asks Problem 5 to repeat Problem 4 using SAP2000. The repository therefore keeps the SAP comparison separate from the Python solver and avoids inventing reference values.

## Wall modelling and meshing

```python
from structural_toolkit.wall import Wall
from structural_toolkit.mesh import create_wall_with_openings_mesh

wall = Wall(4.0, 3.0, 0.23)
wall.add_opening(0.8, 0.9, 1.2, 1.5)
wall.add_opening(2.5, 0.7, 0.8, 1.0)
print(wall.net_area)
create_wall_with_openings_mesh(wall, mesh_size=0.25)
```

## Limitations

- Current structural solver is a **2D pin-jointed truss** solver, not a general frame/shell/solid FEM engine.
- DXF import currently handles LINE geometry; arcs, polylines, blocks and dimensions are not yet mapped to structural semantics.
- Support/load interpretation from CAD layers is planned and should use an explicit documented convention.
- Wall meshing is currently a 2D wall-face mesh. A full 3D solid mesh is a future extension.
- SAP2000 comparison requires exported tables from the user's SAP2000 model; no SAP values are fabricated in this repository.

## Portfolio positioning

This project demonstrates the combination of **civil engineering, structural analysis, Python, CAD automation, 3D modelling and mesh generation** needed for structural-analysis software development. It is intended as a technical portfolio project and not as certified engineering software.

## Validation status

The included CE272 Problem 3 benchmark is executable and regression-tested. The repository also contains the SAP2000 comparison schema and parser utilities. A machine-readable SAP2000 Excel export is required to populate the final comparison CSVs; the available axial-force PDF is retained as external evidence but is not treated as a complete tabular dataset.

## Reproducibility

The project intentionally separates **calculated results** from **reference results**. Reference values are stored under `validation/`, while generated outputs should be written to a separate working directory or explicitly reviewed before committing.
