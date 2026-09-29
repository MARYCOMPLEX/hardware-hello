"""Build the complete textbook and navigation from its single source."""
from pathlib import Path
import html
import re
import markdown

root = Path(__file__).resolve().parent

def slug(value, separator):
    value = re.sub(r"[^\w\u4e00-\u9fff -]", "", value.lower()).strip()
    return value.replace(" ", separator) or "section"

renderer = markdown.Markdown(extensions=["fenced_code", "tables", "toc", "sane_lists"],
    extension_configs={"toc": {"slugify": slug, "toc_depth": "1-3"}})
content = renderer.convert((root / "book.md").read_text())

def navigation(items):
    result = []
    for item in items:
        level = item["level"]
        label = html.escape(item["name"])
        link = f'<a href="#{item["id"]}" class="toc-{level}">{label}</a>'
        children = item.get("children", [])
        if level == 2 and children:
            result.append(f'<details><summary>{link}</summary>{navigation(children)}</details>')
        else:
            result.append(link + navigation(children))
    return "".join(result)

page = (root / "index.template.html").read_text()
page = page.replace("<!-- TOC -->", navigation(renderer.toc_tokens))
page = page.replace("<!-- BOOK_CONTENT -->", content)
(root / "index.html").write_text(page)
print(f"Rendered {len(content):,} HTML characters")
