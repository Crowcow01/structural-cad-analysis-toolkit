import ezdxf
from structural_toolkit.geometry import CADLine

def read_lines(filename, layer=None):
    doc=ezdxf.readfile(filename); lines=[]
    for e in doc.modelspace().query("LINE"):
        if layer is not None and e.dxf.layer != layer: continue
        a,b=e.dxf.start,e.dxf.end
        lines.append(CADLine(float(a.x),float(a.y),float(b.x),float(b.y),e.dxf.layer))
    return lines
