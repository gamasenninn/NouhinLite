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

hkey = 15

#---- Config ------
#template_file = './NouForm.pdf' # template PDF
#output_file = './static/pdf/output.pdf' # output PDF 
#tmp_file = './__tmp.pdf' # temporary

with open('./pdfconf_nou.json','r',encoding="utf-8_sig") as f:
    conf = json.load(f)

'''
conf = {
    'file':{
        'template': './NouForm.pdf',
        'output': './static/pdf/output.pdf',
        'temporary': '__tmp.pdf'
    },
    'DB':{
        'database': './nousei.db',
        'table_head': '納品',
        'table_body':   '納品明細'
    },
    'label':{
        'No':{
            'x':12,
            'y':55
        },
        '商品名':{
            'x':25,
            'y':55
        },
        '商品ロット':{
            'x':83,
            'y':55
        },
        '数量':{
            'x':123,
            'y':55
        },
        '単価':{
            'x':145,
            'y':55
        },
        '金額':{
            'x':165,
            'y':55
        }
    },   
    'header':{
        '納品日':{
            'x':150,
            'y':25,
        },
        '納品先':{
            'x':20,
            'y':33,
        },
        '摘要':{
            'x':15,
            'y':270,
        },
        '合計':{
            'x':165,
            'y':255,
            'f':"{:>20,d}"
        }
    },
    'body':{
        'No':{
            'x':12,
            'y':68,
            'p':9.8
        },
        '商品名':{
            'x':25,
            'y':68,
            'p':9.8
        },
        '商品ロット':{
            'x':83,
            'y':68,
            'p':9.8
        },
        '数量':{
            'x':123,
            'y':68,
            'p':9.8,
            'f':"{:>10,d}"
        },
        '単価':{
            'x':145,
            'y':68,
            'p':9.8,
            'f':"{:>10,d}"
        },
        '金額':{
            'x':165,
            'y':68,
            'p':9.8,
            'f':"{:>20,d}"
        }
    }
}
'''
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
cv.setFont('IPAexGothic', font_size)

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
    nouB['金額'] = nouB['数量']*nouB['単価']
    nouHs[0]['合計'] += nouB['金額']



# --- Make PDF --

def make_pdf(table,key):

    cv.setFillColorRGB(0, 0, 0.4)

    for k,v in conf['label'].items():
        x = v['x']
        y = v['y']
        label = k
        if 'f' in v:
            label = conf['header'][k]['f'].format(v)

        cv.drawString(x*mm, h-y*mm, str(label))
        
        



    for i, nouH in enumerate( nouHs ):
            for k,v in nouH.items():
                    if k in conf['header']:
                        x = conf['header'][k]['x']
                        y = conf['header'][k]['y']
#                        p = conf['header'][k]['p']
                        if 'f' in conf['header'][k]:
                            v = conf['header'][k]['f'].format(v)
                        print(i,k,v,x,y)
#                        cv.drawString(y*mm, h-(x+p*i)*mm, v)
                        cv.drawString(x*mm, h-(y+i)*mm, str(v))
            print("-")

    for i, nouB in enumerate( nouBs ):
            for k,v in nouB.items():
                    if k in conf['body']:
                        x = conf['body'][k]['x']
                        y = conf['body'][k]['y']
                        p = conf['body'][k]['p']
                        if 'f' in conf['body'][k]:
                            v = conf['body'][k]['f'].format(v)
                        print(i,k,v,x,y,p)
#                        cv.drawString(y*mm, h-(x+p*i)*mm, v)
                        cv.drawString(x*mm, h-(y+p*i)*mm, str(v))
            print("-")

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
    
