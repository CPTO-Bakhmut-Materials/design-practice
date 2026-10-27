"""Scribus script: export page 1 of an .sla as PNG (like File → Export → Save as Image).  Args: <sla> <png> [dpi]"""
import sys
import scribus as S
S.openDoc(sys.argv[1])
S.gotoPage(1)
img = S.ImageExport()
img.type = 'PNG'
img.dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 72
img.scale = 100
img.saveAs(sys.argv[2])
S.closeDoc()
