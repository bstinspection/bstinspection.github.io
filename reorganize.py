import os
import re
import shutil

DOCS = "docs"
IMAGES = "images"

RENAME_MAP = {
    "index.md": "index.md",
    "introduction.md": "services.md",
    "introduction_menuid_8.md": "about.md",
    "introduction_menuid_9.md": "production-scope.md",
    "introduction_menuid_10.md": "quality-standard.md",
    "introduction_menuid_11.md": "pricing.md",
    "introduction_menuid_12.md": "terms.md",
    "introduction_menuid_13.md": "order-procedure.md",
    "introduction_menuid_14.md": "privacy.md",
    "introduction_menuid_15.md": "quality-link.md",
    "introduction_menuid_16.md": "reference-reports.md",
    "news.md": "news.md",
    "newsinfo_nid_68.md": "news-2025-address.md",
    "newsinfo_nid_67.md": "news-2025-vietnam.md",
    "newsinfo_nid_62.md": "news-2021-merger.md",
    "contact.md": "contact.md",
}

LINK_FIXES = {
    "introduction_menuid_16.md": "reference-reports.md",
    "introduction_menuid_8.md": "about.md",
    "introduction_menuid_9.md": "production-scope.md",
    "introduction_menuid_10.md": "quality-standard.md",
    "introduction_menuid_11.md": "pricing.md",
    "introduction_menuid_12.md": "terms.md",
    "introduction_menuid_13.md": "order-procedure.md",
    "introduction_menuid_14.md": "privacy.md",
    "introduction_menuid_15.md": "quality-link.md",
    "introduction.md": "services.md",
    "newsinfo_nid_68.md": "news-2025-address.md",
    "newsinfo_nid_67.md": "news-2025-vietnam.md",
    "newsinfo_nid_62.md": "news-2021-merger.md",
}

TITLES = {
    "index.md": "# Guangzhou BST Tech — Home",
    "services.md": "# Our Services — Guangzhou BST Tech",
    "about.md": "# About Us — Guangzhou BST Tech",
    "production-scope.md": "# Production Scope — Guangzhou BST Tech",
    "quality-standard.md": "# Quality Standards — Guangzhou BST Tech",
    "pricing.md": "# Pricing — Guangzhou BST Tech",
    "terms.md": "# Terms and Conditions — Guangzhou BST Tech",
    "order-procedure.md": "# Order Procedure — Guangzhou BST Tech",
    "privacy.md": "# Privacy Policy — Guangzhou BST Tech",
    "quality-link.md": "# Quality Links — Guangzhou BST Tech",
    "reference-reports.md": "# Reference Reports — Guangzhou BST Tech",
    "news.md": "# News — Guangzhou BST Tech",
    "news-2025-address.md": "# BST New Office Address — News",
    "news-2025-vietnam.md": "# Vietnam and Bangladesh Inspection Services — News",
    "news-2021-merger.md": "# Brightsky and Guangzhou BST — News",
    "contact.md": "# Contact Us — Guangzhou BST Tech",
}


def fix_links(text):
    for old, new in LINK_FIXES.items():
        text = text.replace(old, new)
    return text


def fix_heading_levels(text, top_level="##"):
    lines = text.split("\n")
    result = []
    first_header_found = False
    for line in lines:
        if line.startswith("# ") and not first_header_found:
            first_header_found = True
            continue
        if line.startswith("# ") and first_header_found:
            result.append(line)
        else:
            result.append(line)
    return "\n".join(result)


def process_index(content):
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if "MORE" in stripped and "OUR SERVICES" in stripped:
            new_lines.append("## Our Services")
        elif "MORE" in stripped and "NEWS" in stripped:
            new_lines.append("## News")
        else:
            new_lines.append(line)
    return "\n".join(new_lines)


def process_news(content):
    lines = content.split("\n")
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- ") and stripped.count("[") == 1:
            depth = len(line) - len(line.lstrip())
            item = stripped[2:]
            if depth > 0:
                new_lines.append(f"- {item}")
            else:
                new_lines.append(f"- {item}")
        else:
            new_lines.append(line)
    return "\n".join(new_lines)


def process_contact(content):
    lines = content.split("\n")
    new_lines = []
    skip_block = False
    for line in lines:
        if "system/Lib/Code" in line:
            continue
        if "Enter the Code Shown" in line or "If you cannot see" in line:
            continue
        new_lines.append(line)
    text = "\n".join(new_lines)

    text = re.sub(r"\n\|.*\n\|.*\n\|.*", "", text)

    text = text.replace(
        "Email:[Jeffrey@bstinspection.com](mailto:Jeffrey@bstinspection.com)",
        "Email: [Jeffrey@bstinspection.com](mailto:Jeffrey@bstinspection.com)"
    )
    text = text.replace(
        "Email:[info@bstinspection.com](mailto:info@bstinspection.com)",
        "Email: [info@bstinspection.com](mailto:info@bstinspection.com)"
    )

    text = text.strip() + "\n\n---\n\n*Use the form on the original website to send inquiries.*\n"
    return text


def process_services(content):
    text = content
    # Fix '1．' to '1. ' (fullwidth dot to regular)
    text = text.replace("1．", "## 1. ")
    text = text.replace("2．", "## 2. ")
    text = text.replace("3．", "## 3. ")
    text = text.replace("4．", "## 4. ")
    text = text.replace("5．", "## 5. ")
    text = text.replace("6．", "## 6. ")
    text = text.replace("7．", "## 7. ")
    text = text.replace("8．", "## 8. ")
    text = text.replace("9．", "## 9. ")
    # Fix cases where '# ##' was produced (old heading plus our replacement)
    text = text.replace("# ##", "##")
    return text


def process_quality_standard(content):
    text = content

    text = text.replace("Why do you and your clients need quality insurance services?", "## Why do you and your clients need quality insurance services?")
    text = text.replace("What is critical defects, major defects and minor defects?", "## What is critical defects, major defects and minor defects?")
    text = text.replace("What can I find out from the AQL tables?", "## Understanding the AQL Tables")

    text = re.sub(r"^## (\\d+\))", r"### \1", text, flags=re.MULTILINE)

    lines = text.split("\n")
    new_lines = []
    in_table = False
    for line in lines:
        if "## SAPLE SIZE COOELETTERS" in line:
            new_lines.append("### Sample Size Code Letters")
            in_table = False
            continue
        if "## SINGLE SAMPLING PLANS" in line:
            new_lines.append("### Single Sampling Plans for Normal Inspection")
            in_table = False
            continue
        if "|" in line and ("Ac Re" in line or "Lot batch" in line):
            if not in_table:
                new_lines.append("")
                in_table = True
            new_lines.append(line)
            continue
        if in_table and line.strip() == "":
            in_table = False
            new_lines.append(line)
            continue
        if in_table and "|" not in line and line.strip():
            in_table = False
            new_lines.append(line)
            continue
        if in_table:
            new_lines.append(line)
            continue
        new_lines.append(line)
    return "\n".join(new_lines)


def remove_boilerplate(text):
    patterns = [
        r"\nIf you have any question, please contact us directly\. \([^)]+\) Please call us at [^\n]+",
    ]
    for p in patterns:
        text = re.sub(p, "", text)
    return text


def main():
    renamed = {}

    for old_name, new_name in RENAME_MAP.items():
        old_path = os.path.join(DOCS, old_name)
        new_path = os.path.join(DOCS, new_name)
        if old_name != new_name:
            shutil.copy2(old_path, new_path)
            renamed[old_name] = new_name
            print(f"Copied: {old_name} -> {new_name}")

    for new_name in sorted(set(RENAME_MAP.values())):
        filepath = os.path.join(DOCS, new_name)
        if not os.path.exists(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Update links to new filenames FIRST
        content = fix_links(content)

        # Replace generic title with specific title
        content = re.sub(
            r"^# Brightsky Technology Services Co\., Ltd\.?",
            TITLES.get(new_name, "# Guangzhou BST Tech"),
            content,
        )

        # Fix headings for services page
        if new_name == "services.md":
            content = process_services(content)

        # Fix index page
        if new_name == "index.md":
            content = process_index(content)

        # Fix news page
        if new_name == "news.md":
            content = process_news(content)

        # Fix contact page
        if new_name == "contact.md":
            content = process_contact(content)

        # Fix quality standard page tables
        if new_name == "quality-standard.md":
            content = process_quality_standard(content)

        # Remove duplicate "Input time:" line in news detail pages
        if new_name.startswith("news-"):
            content = re.sub(r"\n+Input time:\d{4}-\d{2}-\d{2}", "", content)
            # Fix duplicate headings
            lines = content.split("\n")
            seen_titles = set()
            new_lines = []
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("## ") and stripped in seen_titles:
                    continue
                if stripped.startswith("## ") or stripped.startswith("# "):
                    seen_titles.add(stripped)
                new_lines.append(line)
            content = "\n".join(new_lines)
            # Remove back.jpg line
            content = re.sub(r"\n!\[\]\(images/back\.jpg\)", "", content)

        # Fix duplicate page title line
        content = re.sub(r"\n# Brightsky Technology Services Co\., Ltd\.?", "", content)

        # Remove empty anchor lines like `[](http://...)`
        content = re.sub(r"\n\[\]\(http[^)]+\)", "", content)

        # Remove extra blank lines
        content = re.sub(r"\n{4,}", "\n\n\n", content)

        # Remove boilerplate (except contact.md)
        if new_name not in ("contact.md", "quality-link.md"):
            content = remove_boilerplate(content)

        content = content.strip() + "\n"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Processed: {new_name}")

    # Delete old renamed files
    for old_name, new_name in renamed.items():
        old_path = os.path.join(DOCS, old_name)
        if os.path.exists(old_path):
            os.remove(old_path)
            print(f"Deleted old: {old_name}")

    print("\nDone! All files processed.")


if __name__ == "__main__":
    main()
