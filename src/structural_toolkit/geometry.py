from dataclasses import dataclass
@dataclass(frozen=True)
class CADLine:
    x1: float; y1: float; x2: float; y2: float; layer: str
