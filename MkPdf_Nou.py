from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch, mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

#------ File Congig. --------
template_file = './NouForm.pdf' # template PDF
output_file = './output.pdf' # output PDF 
tmp_file = './__tmp.pdf' # temporary

#------ Make A4 size Canvas
w, h = portrait(A4)
cv = canvas.Canvas(tmp_file, pagesize=(w, h))

#--- Font Config 
font_size = 11
ttf_file = './ipaexg.ttf'
pdfmetrics.registerFont(TTFont('IPAexGothic', ttf_file))
cv.setFont('IPAexGothic', font_size)

# --- Main

cv.setFillColorRGB(0, 0, 0.4)




start = 68
p =9.8




cv.drawString(25*mm, h-start*mm, "これはテストです。")
cv.drawString(25*mm, h-(start+p*1)*mm, "印刷の微調整は")
cv.drawString(25*mm, h-(start+p*2)*mm, "案外難しいものです")
cv.drawString(25*mm, h-(start+p*3)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*4)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*5)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*6)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*7)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*8)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*9)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*11)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*12)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*13)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*14)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*15)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*16)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*17)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*18)*mm, "令和3年 1月 20日")
cv.drawString(25*mm, h-(start+p*19)*mm, "令和3年 1月 20日")


cv.drawString(83*mm, h-(start+40)*mm, "test0001")
cv.drawString(83*mm, h-(start+50)*mm, "test0001")
cv.drawString(83*mm, h-(start+60)*mm, "test0001")
cv.drawString(83*mm, h-(start+70)*mm, "test0001")
cv.drawString(83*mm, h-(start+80)*mm, "test0001")
cv.drawString(83*mm, h-(start+90)*mm, "test0001")
cv.drawString(83*mm, h-(start+100)*mm, "test0001")
cv.drawString(83*mm, h-(start+110)*mm, "test0001")

# ---- temp out 
cv.showPage()
cv.save()

#---- template PDF file read 
template_pdf = PdfFileReader(template_file, strict=False)
template_page = template_pdf.getPage(0)

#---- Concat file
tmp_pdf = PdfFileReader(tmp_file)
template_page.mergePage(tmp_pdf.getPage(0))

#---- Write PDF 
output = PdfFileWriter()
output.addPage(template_page)
with open(output_file, "wb") as fp:
  output.write(fp)
