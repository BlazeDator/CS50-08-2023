from fpdf import FPDF

name = input("Name: ")
pdf = FPDF()
pdf.add_page()

pdf.set_font("Times", size=60)
pdf.cell(txt="CS50 Shirtificate", w=0, h=pdf.eph*.2, align="C")
pdf.ln(1)

pdf.image("shirtificate.png", x=pdf.epw*.1, y=pdf.eph*.3, w=pdf.epw*.9 )

pdf.set_text_color(r=255, g=255, b=255)
pdf.set_font("Times", size=23)
pdf.cell(txt=f"{name} took CS50", w=0, h=pdf.eph*.9, align="C")


pdf.output("shirtificate.pdf")