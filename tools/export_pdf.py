"""Scribus script: export an .sla to PDF/X-4 with bleeds and crop marks.  Args: <sla> <pdf> [icc] [--no-marks]"""
import sys
import scribus as S
MARKS = '--no-marks' not in sys.argv
sys.argv = [a for a in sys.argv if a != '--no-marks']
sla, out = sys.argv[1], sys.argv[2]
S.openDoc(sla)
pdf = S.PDFfile()
pdf.file = out
pdf.version = 15        # PDF/X-4
pdf.outdst = 1          # printer (CMYK)
pdf.embedPDF = 1
pdf.fontEmbedding = 0   # embed
pdf.resolution = 300
pdf.downsample = 0
pdf.quality = 0
pdf.cropMarks = MARKS
pdf.bleedMarks = False
pdf.registrationMarks = False
pdf.colorMarks = False
pdf.markOffset = 3
pdf.useDocBleeds = True
if len(sys.argv) > 3:
    pdf.solidpr = sys.argv[3]
    pdf.imagepr = sys.argv[3]
    pdf.printprofc = sys.argv[3]
    pdf.useprofiles = True
    pdf.useprofiles2 = True
pdf.info = 'KavoBus'
pdf.save()
S.closeDoc()
