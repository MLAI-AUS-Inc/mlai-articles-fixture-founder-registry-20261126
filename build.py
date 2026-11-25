import html
import json
import re
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent
output = root / "dist"
output.mkdir(exist_ok=True)
template = (root / "template.html").read_text()
articles = json.loads((root / "articles.json").read_text())
items = []

def page(path, title, body, prefix):
    destination = output / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    navigation = f'<a href="{prefix}articles/">Articles</a>'
    destination.write_text(template.format(title=html.escape(title), prefix=prefix,
                                           nav=navigation, body=body))

for article in articles:
    slug, title = article["slug"], article["title"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Invalid article slug")
    text = html.escape(article["body"])
    page(f"articles/{slug}/index.html", title,
         f"<article><h1>{html.escape(title)}</h1><p>{text}</p></article>", "../../")
    items.append(f'<li><a href="{slug}/">{html.escape(title)}</a></li>')

page("index.html", "Paperbark Workshop", (root / "home.html").read_text(), "./")
page("articles/index.html", "Articles", f"<h1>Articles</h1><ul>{''.join(items)}</ul>", "../")
for asset in ("style.css", "robots.txt"):
    shutil.copyfile(root / asset, output / asset)
