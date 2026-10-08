import sys
sys.path.append("src")
from structural_toolkit.wall import Wall
w=Wall(4.0,3.0,0.23); w.add_opening(0.8,0.9,1.2,1.5); w.add_opening(2.5,0.7,0.8,1.0)
print(f"Gross area: {w.gross_area:.3f} m²")
print(f"Opening area: {w.opening_area:.3f} m²")
print(f"Net area: {w.net_area:.3f} m²")
print(f"Net volume: {w.volume:.3f} m³")
