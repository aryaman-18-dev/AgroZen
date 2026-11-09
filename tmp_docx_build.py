from html.parser import HTMLParser
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pathlib import Path
src=Path('AgroZen_Project_Report_Draft.html').read_text(encoding='utf-8')
out=Document(); sec=out.sections[0]; sec.top_margin=Inches(.8); sec.bottom_margin=Inches(.8); sec.left_margin=Inches(1); sec.right_margin=Inches(1)
style=out.styles['Normal']; style.font.name='Times New Roman'; style.font.size=Pt(12)
class P(HTMLParser):
 def __init__(self): super().__init__(); self.stack=[]; self.buf=''; self.in_svg=False; self.table=[]; self.row=None
 def flush(self,tag=None):
  t=' '.join(self.buf.split()); self.buf=''
  if not t:return
  if self.table is not None and self.row is not None:self.row.append(t);return
  if self.in_svg:return
  if self.stack and self.stack[-1]=='h1': p=out.add_heading(t,0);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  elif self.stack and self.stack[-1]=='h2': p=out.add_heading(t,1);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
  elif self.stack and self.stack[-1]=='h3': out.add_heading(t,2)
  elif self.stack and self.stack[-1]=='li': out.add_paragraph(t,style='List Bullet')
  else: out.add_paragraph(t)
 def handle_starttag(self,tag,attrs):
  if tag in ('p','h1','h2','h3','li'): self.flush();self.stack.append(tag)
  elif tag=='br': self.buf+='\n'
  elif tag=='svg': self.flush();self.in_svg=True
  elif tag=='table': self.flush();self.table=[]
  elif tag=='tr': self.row=[]
 def handle_endtag(self,tag):
  if tag=='svg': self.in_svg=False; out.add_paragraph('[Diagram: refer to system flow / architecture diagram in HTML draft.]')
  elif tag=='tr' and self.row is not None:self.table.append(self.row);self.row=None
  elif tag=='table':
   if self.table:
    tb=out.add_table(rows=0,cols=max(map(len,self.table)));tb.style='Table Grid'
    for row in self.table:
     cells=tb.add_row().cells
     for i,v in enumerate(row):cells[i].text=v
   self.table=None
  elif tag in ('p','h1','h2','h3','li'):
   self.flush(tag)
   if self.stack:self.stack.pop()
 def handle_data(self,data):
  if not self.in_svg:self.buf+=data
parser=P();parser.feed(src);parser.flush()
out.save('AgroZen_Project_Report.docx')
