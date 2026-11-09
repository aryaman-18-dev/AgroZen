from pathlib import Path
import re, textwrap, html
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted, KeepTogether

folder=Path('PROJECT_DOCUMENTATION')
out=folder/'AgroZen_Project_Documentation_Complete.pdf'
files=[folder/'README.md']+sorted(folder.glob('*.md'),key=lambda p:p.name)
# Avoid duplicate README entry from glob.
seen=set(); files=[p for p in files if not (p.name in seen or seen.add(p.name))]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitleX',parent=styles['Title'],fontName='Helvetica-Bold',fontSize=25,leading=31,textColor=colors.HexColor('#185a37'),alignment=TA_CENTER,spaceAfter=18))
styles.add(ParagraphStyle(name='SubX',parent=styles['Normal'],fontName='Helvetica',fontSize=12,leading=17,textColor=colors.HexColor('#394a42'),alignment=TA_CENTER))
styles.add(ParagraphStyle(name='H1X',parent=styles['Heading1'],fontName='Helvetica-Bold',fontSize=16,leading=20,textColor=colors.HexColor('#185a37'),spaceBefore=8,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='H2X',parent=styles['Heading2'],fontName='Helvetica-Bold',fontSize=12,leading=15,textColor=colors.HexColor('#28664a'),spaceBefore=7,spaceAfter=5,keepWithNext=True))
styles.add(ParagraphStyle(name='H3X',parent=styles['Heading3'],fontName='Helvetica-Bold',fontSize=10,leading=12,textColor=colors.HexColor('#335e49'),spaceBefore=6,spaceAfter=4,keepWithNext=True))
styles.add(ParagraphStyle(name='BodyX',parent=styles['BodyText'],fontName='Helvetica',fontSize=8.7,leading=11.5,spaceAfter=5,splitLongWords=True))
styles.add(ParagraphStyle(name='SmallX',parent=styles['BodyText'],fontName='Helvetica',fontSize=7.3,leading=9,splitLongWords=True))
styles.add(ParagraphStyle(name='CodeX',fontName='Courier',fontSize=6.3,leading=8,backColor=colors.HexColor('#f1f4f2'),borderColor=colors.HexColor('#d4dfd8'),borderWidth=.4,borderPadding=5,spaceBefore=3,spaceAfter=7))
styles.add(ParagraphStyle(name='BulletX',parent=styles['BodyX'],leftIndent=12,firstLineIndent=-8,bulletIndent=0,spaceAfter=3))
styles.add(ParagraphStyle(name='CoverSmallX',parent=styles['Normal'],fontName='Helvetica',fontSize=9,leading=13,textColor=colors.HexColor('#394a42'),alignment=TA_CENTER))

def inline(s):
    parts=re.split(r'(`[^`]*`)',s)
    rendered=[]
    for part in parts:
        if part.startswith('`') and part.endswith('`') and len(part)>=2:
            rendered.append('<font name="Courier" size="7.4">'+html.escape(part[1:-1],quote=False)+'</font>')
            continue
        text=html.escape(part,quote=False)
        text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
        text=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',text)
        text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<u>\1</u> (\2)',text)
        rendered.append(text)
    return ''.join(rendered)

def wrapped_code(lines,width=100):
    out=[]
    for line in lines:
        if len(line)<=width: out.append(line); continue
        indent=len(line)-len(line.lstrip())
        out.extend(textwrap.wrap(line,width=width,subsequent_indent=' '*min(indent+2,12),replace_whitespace=False,drop_whitespace=False,break_long_words=True) or [''])
    return '\n'.join(out)

def parse_table(lines):
    rows=[]
    for line in lines:
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        if cells and all(re.fullmatch(r':?-{3,}:?',c.replace(' ','')) for c in cells): continue
        rows.append([Paragraph(inline(c),styles['SmallX']) for c in cells])
    if not rows:return None
    n=max(map(len,rows));
    for row in rows: row.extend([Paragraph('',styles['SmallX'])]*(n-len(row)))
    widths=[(A4[0]-34*mm)/n]*n
    t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dcebe1')),
        ('TEXTCOLOR',(0,0),(-1,0),colors.HexColor('#163e2b')),
        ('GRID',(0,0),(-1,-1),.35,colors.HexColor('#aab8af')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
    ]))
    return t

story=[Spacer(1,42*mm),Paragraph('AgroZen Project Documentation',styles['CoverTitleX']),Paragraph('Complete source-grounded project guide',styles['SubX']),Spacer(1,12*mm),Paragraph('Combined from every Markdown file in PROJECT_DOCUMENTATION',styles['CoverSmallX']),Spacer(1,8*mm),Paragraph(f'{len(files)} Markdown files · beginner guide, architecture, source inventory, API routes, data models, workflows, setup, audit and interview preparation',styles['CoverSmallX']),PageBreak(),Paragraph('Contents',styles['H1X'])]
for f in files: story.append(Paragraph('• '+inline(f.stem.replace('_',' ')),styles['BodyX']))
story.append(PageBreak())
for file_index,path in enumerate(files):
    story.append(Paragraph(inline(path.stem.replace('_',' ')),styles['H1X']))
    lines=path.read_text(encoding='utf-8-sig').splitlines()
    i=0; para=[]
    def flush_para():
        nonlocal_dummy=None
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            if para:
                story.append(Paragraph(inline(' '.join(para)),styles['BodyX']));para=[]
            lang=line[3:].strip(); i+=1; block=[]
            while i<len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]);i+=1
            story.append(Paragraph('<b>'+inline(('Mermaid diagram source' if lang=='mermaid' else (lang+' code' if lang else 'Code')) )+'</b>',styles['SmallX']))
            story.append(Preformatted(wrapped_code(block),styles['CodeX']))
            i+=1; continue
        if not line.strip():
            if para: story.append(Paragraph(inline(' '.join(para)),styles['BodyX']));para=[]
            i+=1;continue
        if line.startswith('|'):
            if para: story.append(Paragraph(inline(' '.join(para)),styles['BodyX']));para=[]
            table_lines=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i]);i+=1
            t=parse_table(table_lines)
            if t: story.append(t);story.append(Spacer(1,5))
            continue
        hm=re.match(r'^(#{1,6})\s+(.*)$',line)
        if hm:
            if para: story.append(Paragraph(inline(' '.join(para)),styles['BodyX']));para=[]
            level=len(hm.group(1));sty=styles['H1X'] if level<=2 else styles['H2X'] if level==3 else styles['H3X']
            story.append(Paragraph(inline(hm.group(2)),sty));i+=1;continue
        if line.lstrip().startswith('- ') or line.lstrip().startswith('* '):
            if para: story.append(Paragraph(inline(' '.join(para)),styles['BodyX']));para=[]
            text=line.lstrip()[2:]
            story.append(Paragraph('• '+inline(text),styles['BulletX']));i+=1;continue
        if re.match(r'^\s*\d+\.\s+',line):
            if para: story.append(Paragraph(inline(' '.join(para)),styles['BodyX']));para=[]
            m=re.match(r'^\s*(\d+)\.\s+(.*)',line)
            story.append(Paragraph(m.group(1)+'. '+inline(m.group(2)),styles['BulletX']));i+=1;continue
        if line.startswith('> '):
            if para: story.append(Paragraph(inline(' '.join(para)),styles['BodyX']));para=[]
            story.append(Paragraph('<i>'+inline(line[2:])+'</i>',styles['BodyX']));i+=1;continue
        para.append(line.strip());i+=1
    if para: story.append(Paragraph(inline(' '.join(para)),styles['BodyX']))
    if file_index<len(files)-1: story.append(PageBreak())

def footer(canvas,doc):
    canvas.saveState();canvas.setFont('Helvetica',7);canvas.setFillColor(colors.HexColor('#5c7065'))
    canvas.drawString(17*mm,9*mm,'AgroZen Project Documentation')
    canvas.drawRightString(A4[0]-17*mm,9*mm,str(doc.page))
    canvas.restoreState()

doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=17*mm,leftMargin=17*mm,topMargin=16*mm,bottomMargin=16*mm,title='AgroZen Project Documentation Complete',author='AgroZen Project Team',allowSplitting=1)
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(f'Created {out} from {len(files)} markdown files ({sum(len(p.read_text(encoding="utf-8-sig")) for p in files):,} characters).')
