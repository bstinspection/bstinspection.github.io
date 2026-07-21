import os, time, logging, re
from urllib.parse import urlparse, urljoin
from collections import deque
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://bstinspection.com/"
OUTPUT_DIR = "output"
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
LOG_FILE = "crawl.log"
DELAY = 1
TIMEOUT = 15

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()])

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})

visited_urls = set()
downloaded_images = set()
queue = deque()

def normalize_url(url):
    p = urlparse(url)
    path = p.path.rstrip("/") or "/"
    return f"{path}?{p.query}" if p.query else path

def url_without_fragment(url):
    return urlparse(url)._replace(fragment="").geturl()

def is_same_domain(url):
    netloc = urlparse(url).netloc
    return netloc in ("bstinspection.com", "www.bstinspection.com", "")

def is_image_url(url):
    return any(urlparse(url).path.lower().endswith(e) for e in (".jpg",".jpeg",".png",".gif",".bmp",".webp",".svg"))

def is_page_url(url):
    path = urlparse(url).path.lower()
    if any(path.endswith(e) for e in (".jpg",".jpeg",".png",".gif",".bmp",".webp",".svg",".css",".js",".ico",".pdf",".zip",".mp4",".avi",".doc",".docx",".xls",".xlsx")):
        return False
    return True

def filename_from_url(url):
    p = urlparse(url)
    path = p.path.lstrip("/")
    if not path or path.endswith("/"): path += "index.asp"
    base, ext = os.path.splitext(path)
    if not ext: path += ".asp"
    if p.query:
        path = f"{base}_{p.query.replace('=','_').replace('&','_')}{ext}"
    return path

def ensure_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGE_DIR, exist_ok=True)

def save_page(url, content):
    path = filename_from_url(url)
    full = os.path.join(OUTPUT_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "wb") as f: f.write(content)
    logging.info(f"  Saved page: {os.path.relpath(full, OUTPUT_DIR)}")

def download_file(url, referer=None):
    if url in downloaded_images: return
    downloaded_images.add(url)
    try:
        hdrs = {"Referer": referer} if referer else {}
        resp = session.get(url, headers=hdrs, timeout=TIMEOUT)
        resp.raise_for_status()
        fp = urlparse(url).path.lstrip("/")
        full = os.path.join(OUTPUT_DIR, fp)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f: f.write(resp.content)
        logging.info(f"  Saved: {os.path.relpath(full, OUTPUT_DIR)}")
    except Exception as e:
        logging.warning(f"  Failed {url}: {e}")

def extract_urls(url, html):
    soup = BeautifulSoup(html, "html.parser")
    found = set()
    for tag in soup.find_all(["a","img"], href=True) + soup.find_all(["a","img"], src=True):
        raw = tag.get("href") or tag.get("src")
        if not raw or raw.startswith("#") or raw.startswith("javascript") or raw.startswith("mailto"): continue
        full = urljoin(url, raw)
        if is_same_domain(full): found.add(full)
    for s in soup.find_all("script"):
        src = s.get("src")
        if src:
            full = urljoin(url, src)
            if is_same_domain(full): found.add(full)
    for l in soup.find_all("link"):
        href = l.get("href")
        if href:
            full = urljoin(url, href)
            if is_same_domain(full): found.add(full)
    return found

def crawl(start_url):
    queue.append(start_url)
    visited_urls.add(normalize_url(start_url))
    while queue:
        url = queue.popleft()
        logging.info(f"Crawling: {url}")
        try:
            resp = session.get(url, timeout=TIMEOUT)
            resp.raise_for_status()
        except Exception as e:
            logging.warning(f"  Failed {url}: {e}"); continue
        content = resp.content
        if is_image_url(url): download_file(url); continue
        save_page(url, content)
        found = extract_urls(url, content)
        new = set()
        for fu in found:
            fu = url_without_fragment(fu)
            n = normalize_url(fu)
            if n in visited_urls: continue
            visited_urls.add(n)
            if is_image_url(fu): download_file(fu, referer=url)
            elif is_page_url(fu): queue.append(fu); new.add(fu)
            else: download_file(fu, referer=url)
        if new: logging.info(f"  Discovered {len(new)} new: {[normalize_url(u) for u in new]}")
        time.sleep(DELAY)

if __name__ == "__main__":
    ensure_dirs()
    logging.info(f"Starting crawl of {BASE_URL}")
    crawl(BASE_URL)
    logging.info(f"Done. Visited {len(visited_urls)} URLs, {len(downloaded_images)} files.")
