"""Extract text blocks from an HTML file without executing it. Usage: python3 -I htmltext.py file.html"""
import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.skip=0; s.out=[]; s.buf=[]
    def handle_starttag(s, t, a):
        if t in ('script','style','noscript','svg','template'): s.skip+=1
        if t in ('p','div','h1','h2','h3','h4','h5','h6','li','a','span','button','br','section','figcaption','label','option','td','th'): s.flush()
    def handle_endtag(s, t):
        if t in ('script','style','noscript','svg','template'): s.skip=max(0,s.skip-1)
        s.flush()
    def handle_data(s, d):
        if not s.skip: s.buf.append(d)
    def flush(s):
        t=re.sub(r'\s+',' ',''.join(s.buf).replace(' ',' ').replace('​','')).strip()
        if t: s.out.append(t)
        s.buf=[]
def blocks(path):
    p=P(); p.feed(open(path,encoding='utf-8',errors='replace').read()); p.flush(); return p.out
if __name__=='__main__':
    for b in blocks(sys.argv[1]): print(b)
