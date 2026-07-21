import os, re

DOCS = "docs"

def read(file):
    with open(os.path.join(DOCS, file), "r", encoding="utf-8") as f:
        return f.read()

def write(file, content):
    with open(os.path.join(DOCS, file), "w", encoding="utf-8") as f:
        f.write(content)

# ===== 1. Fix double headings (# ## -> ##) in all files =====
for fname in os.listdir(DOCS):
    if not fname.endswith(".md"):
        continue
    content = read(fname)
    content = content.replace("# ##", "##")
    content = content.replace("# #", "##")
    write(fname, content)

# ===== 2. Fix quality-standard.md AQL tables =====
content = read("quality-standard.md")

# Fix duplicate "# SINGLE SAMPLING" line
content = re.sub(r"# SINGLE SAMPLING PLANS FOR NORMAL INSPECTION\n\n\*\*Sample size", "### Single Sampling Plans for Normal Inspection\n\n**Sample size", content)

# Insert the rebuilt Sample Size Code Letters table
aql_code_table = """### Sample Size Code Letters

| Lot batch size | S-1 | S-2 | S-3 | S-4 | I | II | III |
|---|---|---|---|---|---|---|---|
| 2 to 8 | A | A | A | A | A | A | B |
| 9 to 15 | A | A | A | A | A | B | C |
| 16 to 25 | A | A | B | B | B | C | D |
| 26 to 50 | A | B | B | C | C | D | E |
| 51 to 90 | B | B | C | C | C | E | F |
| 91 to 150 | B | B | C | D | D | F | G |
| 151 to 280 | B | C | D | E | E | G | H |
| 281 to 500 | B | C | D | E | F | H | J |
| 501 to 1200 | C | C | E | F | G | J | K |
| 1201 to 3200 | C | D | E | G | H | K | L |
| 3201 to 10000 | C | D | F | G | J | L | M |
| 10001 to 35000 | C | D | F | H | K | M | N |
| 35001 to 150000 | D | E | G | J | L | N | P |
| 150001 to 500000 | D | E | G | J | M | P | Q |
| 500001 and over | D | E | H | K | N | Q | R |

"""

# Replace from "### Sample Size Code Letters" to the broken table + "Practically" text
content = re.sub(
    r"### Sample Size Code Letters\n\n\n\*\*Lot batch size.*?(?=### Single Sampling Plans|$)",
    aql_code_table,
    content,
    flags=re.DOTALL
)

# Build Simplified Single Sampling table
single_sampling = """### Single Sampling Plans for Normal Inspection

| Code | Size | AQL 0.40 | AQL 0.65 | AQL 1.0 | AQL 1.5 | AQL 2.5 | AQL 4.0 | AQL 6.5 |
|---|---|---|---|---|---|---|---|---|
| | | Ac Re | Ac Re | Ac Re | Ac Re | Ac Re | Ac Re | Ac Re |
| A | 2 | | | | | 0 1 | | |
| B | 3 | | | | | 0 1 | | |
| C | 5 | | | 0 1 | | 0 1 | | |
| D | 8 | | | | 1 2 | 1 2 | 2 3 | |
| E | 13 | | | 1 2 | 2 3 | 3 4 | | |
| F | 20 | | 0 1 | 1 2 | 2 3 | 3 4 | 5 6 | |
| G | 32 | 0 1 | 1 2 | 2 3 | 3 4 | 5 6 | 7 8 | |
| H | 50 | 1 2 | 2 3 | 3 4 | 5 6 | 7 8 | 10 11 | 14 15 |
| J | 80 | 1 2 | 2 3 | 3 4 | 5 6 | 7 8 | 10 11 | 14 15 |
| K | 125 | 1 2 | 2 3 | 3 4 | 5 6 | 7 8 | 10 11 | 14 15 |
| L | 200 | 2 3 | 3 4 | 5 6 | 7 8 | 10 11 | 14 15 | 21 22 |
| M | 315 | 3 4 | 5 6 | 7 8 | 10 11 | 14 15 | 21 22 | 21 22 |
| N | 500 | 5 6 | 7 8 | 10 11 | 14 15 | 21 22 | | |
| P | 800 | 7 8 | 10 11 | 14 15 | 21 22 | | | |
| Q | 1250 | 10 11 | 14 15 | 21 22 | | | | |
| R | 2000 | 14 15 | 21 22 | | | | | |

"""

content = re.sub(
    r"### Single Sampling Plans for Normal Inspection\n\n\*\*Sample size code letter.*?(?=\n\n\nPractically|\n\n# |\n\n## |$)",
    single_sampling,
    content,
    flags=re.DOTALL
)

# Restore any text lost after the table
if "Practically" not in content:
    content += "\n\nPractically, BST Quality Standards use the MIL-STD-105E tables that are summarized above.\n"

write("quality-standard.md", content)

# ===== 3. Fix services.md sub-heading levels (## In general -> ### In general) =====
content = read("services.md")
content = content.replace("\n## In general", "\n### In general")
content = re.sub(r"\n## (\\d+\\. .*?)\n", r"\n## \1\n", content)  
write("services.md", content)

# ===== 4. Fix order-procedure.md headings =====
content = read("order-procedure.md")
content = content.replace("# First:", "## 1. First:")
content = content.replace("# Second:", "## 2. Second:")
content = content.replace("# Third:", "## 3. Third:")
content = content.replace("# Fourth:", "## 4. Fourth:")
write("order-procedure.md", content)

# ===== 5. Add space between date and link in lists (all files) =====
for fname in os.listdir(DOCS):
    if not fname.endswith(".md"):
        continue
    content = read(fname)
    content = re.sub(r"(\d{4}-\d{2}-\d{2})(\[)", r"\1 \2", content)
    write(fname, content)

# ===== 6. Remove boilerplate "If you have any question..." from all files except contact.md =====
for fname in os.listdir(DOCS):
    if not fname.endswith(".md") or fname == "contact.md":
        continue
    content = read(fname)
    content = re.sub(
        r"\nIf you have any question, please contact us directly\. \([^)]+\) Please call us at [^\n]+",
        "",
        content,
    )
    write(fname, content)

# ===== 7. Fix news detail pages - remove duplicate titles and fix heading =====
for fname in ["news-2025-address.md", "news-2025-vietnam.md", "news-2021-merger.md"]:
    content = read(fname)
    lines = content.split("\n")
    # Remove duplicate subtitle that matches or is close to the title
    cleaned = []
    skip_next = False
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        if line.strip().startswith("##") and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            # Check if the next line is a subtitle similar to the heading text
            if next_line and next_line == line.strip().lstrip("#").strip():
                # We have a heading followed by an identical subtitle line
                cleaned.append(line)
                skip_next = True
                continue
        cleaned.append(line)
    content = "\n".join(cleaned)

    # Remove empty ## headers
    content = re.sub(r"## \s*\n", "", content)

    # Ensure first ## after title is relevant
    write(fname, content)

# ===== 8. Strip trailing whitespace, normalize blank lines =====
for fname in os.listdir(DOCS):
    if not fname.endswith(".md"):
        continue
    content = read(fname)
    content = re.sub(r" +\n", "\n", content)
    content = re.sub(r"\n{4,}", "\n\n\n", content)
    content = content.strip() + "\n"
    write(fname, content)

print("Cleanup complete!")
