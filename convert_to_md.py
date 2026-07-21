import os, re, logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import html2text

INPUT_DIR = "output"
OUTPUT_DIR = "docs"
LOG_FILE = "convert.log"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()])

LINK_MAP = {"index.asp": "index.md"}
for mid in range(8, 17):
    LINK_MAP[f"introduction.asp?menuid={mid}"] = f"introduction_menuid_{mid}.md"
for nid in (62, 67, 68):
    LINK_MAP[f"newsinfo.asp?nid={nid}"] = f"newsinfo_nid_{nid}.md"
LINK_MAP.update({"introduction.asp": "introduction.md", "news.asp": "news.md", "contact.asp": "contact.md"})

def fix_links(md):
    def repl(m):
        raw = m.group(1)
        p = urlparse(raw)
        full = p.path + ("?" + p.query if p.query else "")
        target = LINK_MAP.get(full)
        if target:
            return m.group(0).replace(raw, target + ("#" + p.fragment if p.fragment else ""))
        return m.group(0)
    return re.sub(r'(?<=\]\()([^)]+)(?=\))', repl, md)

def extract_content(soup, fname):
    if fname == "index.asp":
        parts = []
        for cls in ("ban_font", "ind_content"):
            el = soup.find("div", class_=cls)
            if el: parts.append(str(el))
        return BeautifulSoup("\n".join(parts), "html.parser") if parts else None
    for cls in ("content", "contact"):
        el = soup.find("div", class_=cls)
        if el: return el
    return None

def convert():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    conv = html2text.HTML2Text()
    conv.body_width = 0
    conv.ignore_links = False
    conv.ignore_images = False
    conv.ignore_emphasis = False
    conv.reference_links = False
    conv.ul_item_mark = "-"

    files = sorted(os.path.join(r, f) for r, _, fs in os.walk(INPUT_DIR) for f in fs if f.lower().endswith(".asp"))
    logging.info(f"Converting {len(files)} files")

    for asp in files:
        rel = os.path.relpath(asp, INPUT_DIR)
        logging.info(f"Converting: {rel}")
        with open(asp, "rb") as f: raw = f.read()
        try: text = raw.decode("utf-8")
        except: text = raw.decode("gbk", errors="replace")
        soup = BeautifulSoup(text, "html.parser")
        tag = extract_content(soup, rel.replace("\\","/"))
        if tag is None:
            body = soup.find("body")
            if body: tag = body
            else: continue
        md = conv.handle(str(tag))
        md = re.sub(r"\n{4,}", "\n\n\n", md).strip()
        md = fix_links(md)
        title = soup.find("title")
        if title: md = f"# {title.get_text(strip=True)}\n\n{md}"
        name = os.path.splitext(rel.replace("\\","/"))[0] + ".md"
        for src, dst in LINK_MAP.items():
            if src.replace("?","_").replace("=","_").replace("&","_") in rel.replace("\\","/"):
                name = dst; break
        path = os.path.join(OUTPUT_DIR, name)
        with open(path, "w", encoding="utf-8") as f: f.write(md + "\n")
        logging.info(f"  -> {name}")
    logging.info(f"Done. Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    convert()
