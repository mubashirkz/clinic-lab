from fpdf import FPDF
import glob
pdf = FPDF()
pdf.add_page()
pdf.set_font("Helvetica","B",20)
pdf.cell(0,20,"Clinic lab Evidence",ln=True,align="C")
pdf.set_font("Helvetica","",11)
pdf.multi_cell(0,7,"Evidence: README, network proof, snapshot logs")
for img in sorted(glob.glob("docs/*.png")):
    pdf.add_page()
    pdf.set_font("Helvetica","B",12)
    pdf.cell(0,10,img,ln=True,align="C")
    pdf.image(img,x=10,y=20,w=190)
pdf.output("lab-evidence.pdf")
print("Fixed PDF done")
