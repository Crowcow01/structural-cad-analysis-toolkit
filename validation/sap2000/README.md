# SAP2000 validation schema

SAP2000 is an external benchmark for the toolkit; it is not reimplemented internally.

Export these SAP2000 tables as CSV and normalize them to:

- `member_forces.csv`: `member_id,force_kN`
- `joint_displacements.csv`: `node_id,Ux_mm,Uy_mm`
- `reactions.csv`: `node_id,Rx_kN,Ry_kN`

Use `structural_toolkit.validation.compare_results()` to compare a Python CSV with the corresponding SAP2000 CSV.

The CE272 assignment specifically asks the SAP2000 repeat as Problem 5. The repository intentionally does not fabricate values when the source workbook/table export is unavailable.
