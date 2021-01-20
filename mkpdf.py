# -*- coding: utf-8 -*-

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import inch, mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sqlite3
from sqlwrap import *
import json
import sys


args = sys.argv
conf_file = './pdf_nouhin.conf'
hkey = 15

print(args)

if len(args) > 2:
    conf_file = './'+args[1]+'.conf'
    hkey = int(args[2])

#---- Configファイルロード ------
with open('./pdf_nouhin.conf','r',encoding="utf-8_sig") as f:
    conf = json.load(f)

#------ File Congig. --------
template_file = conf['file']['template']
output_file = conf['file']['output'] 
tmp_file = conf['file']['temporary']

#------ Make A4 size Canvas
w, h = portrait(A4)
cv = canvas.Canvas(tmp_file, pagesize=(w, h))

#--- Font Config 
font_size = 11
ttf_file = './ipaexg.ttf'
pdfmetrics.registerFont(TTFont('IPAexGothic', ttf_file))
#cv.setFont('IPAexGothic', font_size)
cv.setFont(conf['default']['font'],conf['default']['fontsize'])


#---- DB read ----

db = conf['DB']['database']
conn = sqlite3.connect(db)

htable = conf['DB']['table_head']
btable = conf['DB']['table_body']

nouHs = dict_select_all_key(conn, htable,{'ID':hkey }, 'ID')
nouBs = dict_select_all_key(conn, btable,{'納品ID':hkey }, '納品ID')

nouHs[0]['合計']=0
for i,nouB in enumerate(nouBs):
    nouB['No'] = i + 1
    try:
        nouB['金額'] = int(nouB['数量']*nouB['単価'])
        nouHs[0]['合計'] += nouB['金額']
    except:
        pass


# --- Make PDF --



def make_pdf(table,key):

    cv.setFillColorRGB(0, 0, 0.4)

#    cv.line(10*mm,h-10*mm,100*mm,h-100*mm)

    for k,v in conf['label'].items():
        x = v['x']
        y = v['y']
        label = k
        if 'f' in v:
            label = conf['label'][k]['f'].format(v)
        if 's' in v:
            font_size = conf['label'][k]['s']
        else:
            font_size = conf['default']['fontsize']

        if 'f' in conf['label'][k]:
            v = conf['label'][k]['f'].format(v)
            
        cv.setFont(conf['default']['font'],font_size)
        cv.drawString(x*mm, h-y*mm, str(label))
             
    for i, nouH in enumerate( nouHs ):
            for k,v in nouH.items():
                    if k in conf['header']:
                        x = conf['header'][k]['x']
                        y = conf['header'][k]['y']
#                        p = conf['header'][k]['p']
                        if 'f' in conf['header'][k]:
                            v = conf['header'][k]['f'].format(v)

                        if 's' in conf['header'][k]:
                            font_size = conf['header'][k]['s']
                        else:
                            font_size = conf['default']['fontsize']
                           
                        cv.setFont(conf['default']['font'],font_size)
                            
#                        print(i,k,v,x,y)
#                        cv.drawString(y*mm, h-(x+p*i)*mm, v)
                        cv.drawString(x*mm, h-(y+i)*mm, str(v))
#            print("-")

    for i, nouB in enumerate( nouBs ):
            for k,v in nouB.items():
                    if k in conf['body']:
                        x = conf['body'][k]['x']
                        y = conf['body'][k]['y']
                        p = conf['body'][k]['p']
                        if 'f' in conf['body'][k]:
                            v = conf['body'][k]['f'].format(v)
#                        print(i,k,v,x,y,p)
#                        cv.drawString(y*mm, h-(x+p*i)*mm, v)
                        cv.drawString(x*mm, h-(y+p*i)*mm, str(v))
#            print("-")

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

if __name__ == "__main__":
    make_pdf('test_table','test_key')
    
