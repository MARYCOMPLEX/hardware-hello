from pathlib import Path
import html,re
root=Path(__file__).parent
md=(root/'book.md').read_text()

def inline(s):
    s=html.escape(s, quote=False)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',s)
    return s

def slug(s):
    x=re.sub(r'[^\w\u4e00-\u9fff -]','',s.lower()).strip().replace(' ','-')
    return x or 'section'

out=[]; toc=[]; i=0; in_code=False; code=[]; list_type=None; table=False
lines=md.splitlines()
def close_list():
    global list_type
    if list_type: out.append(f'</{list_type}>'); list_type=None
for line in lines:
    if line.startswith('```'):
        close_list()
        if not in_code:
            in_code=True; code=[]
        else:
            out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>'); in_code=False
        continue
    if in_code:
        code.append(line); continue
    if not line.strip():
        close_list(); continue
    if line.startswith('> '):
        close_list(); out.append('<blockquote>'+inline(line[2:])+'</blockquote>'); continue
    m=re.match(r'^(#{1,6})\s+(.+)$',line)
    if m:
        close_list(); level=len(m.group(1)); text=m.group(2).strip(); ident=slug(text)
        if any(x[0]==ident for x in toc): i+=1; ident=f'{ident}-{i}'
        if level<=2: toc.append((ident,text,level))
        out.append(f'<h{level} id="{ident}">{inline(text)}</h{level}>'); continue
    if line.startswith('|') and line.endswith('|'):
        cells=[x.strip() for x in line.strip('|').split('|')]
        if all(re.fullmatch(r':?-+:?',x) for x in cells): continue
        if not table: out.append('<table><thead><tr>'+''.join('<th>'+inline(x)+'</th>' for x in cells)+'</tr></thead><tbody>'); table=True
        else: out.append('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in cells)+'</tr>')
        continue
    if table:
        out.append('</tbody></table>'); table=False
    m=re.match(r'^[-*]\s+(.+)$',line)
    if m:
        if list_type!='ul': close_list(); out.append('<ul>'); list_type='ul'
        out.append('<li>'+inline(m.group(1))+'</li>'); continue
    m=re.match(r'^\d+\.\s+(.+)$',line)
    if m:
        if list_type!='ol': close_list(); out.append('<ol>'); list_type='ol'
        out.append('<li>'+inline(m.group(1))+'</li>'); continue
    close_list(); out.append('<p>'+inline(line)+'</p>')
close_list()
if table: out.append('</tbody></table>')
content='\n'.join(out)
toc_html=''.join(f'<a href="#{ident}" class="toc-{level}">{html.escape(text)}</a>' for ident,text,level in toc if level<=2)
base=(root/'index.template.html').read_text()
base=base.replace('<!-- TOC -->',toc_html).replace('<!-- BOOK_CONTENT -->',content)
(root/'index.html').write_text(base)
print(f'rendered {len(content)} chars, {len(toc)} headings')
