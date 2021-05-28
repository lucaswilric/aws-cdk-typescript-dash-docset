import logging
import sqlite3
import string
from collections import defaultdict

import bs4
import requests
from bs4 import BeautifulSoup, Tag
from lxml import html

from pathlib import Path

SOURCE_DOCUMENT_BASE_DIR = "tmp/download"
TOC_FILE = f"{SOURCE_DOCUMENT_BASE_DIR}/api/toc.html"
DESTINATION_DOCUMENT_BASE_DIR = "aws-cdk-ts.docset/Contents/Resources/Documents"
DOCSET_DATABASE = "aws-cdk-ts.docset/Contents/Resources/docSet.dsidx"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


db = sqlite3.connect(DOCSET_DATABASE, isolation_level=None)
db.isolation_level = None

db.execute("DELETE FROM searchIndex")
db.execute("VACUUM")

toc_content = open(TOC_FILE, "r").read()
tree = html.fromstring(toc_content)

def clean_article(soup):
    # Get rid of some junk & noise
    soup.find("header").decompose()
    soup.find('div', {'class': 'sidenav hide-when-search'}).decompose()
    for s in soup.select('script'):
        s.decompose()

    # Get rid of wide margins
    soup.find('div', {'class': 'article row grid-right'})['class'] = ''

module_sections = tree.xpath("//div[@id='toc']/ul/li")
for module_section in module_sections:
    # There should be only one link directly under this "li" tag
    module_link = module_section.xpath("a")[0]
    module_path = "api/" + module_link.attrib["href"]
    logger.info(f"Parsing {module_path}")
    module_title = module_link.attrib["title"]
    output_path = f"api/{module_title}.html"
    output_dir = f"api/{module_title}"
    name = module_link.attrib["title"]
    entry_type = "Module"

    soup = BeautifulSoup(
        open(f"{SOURCE_DOCUMENT_BASE_DIR}/{module_path}", "r").read(), "html.parser"
    )

    clean_article(soup)

    article_tag = soup.find("article")
    article_parent = article_tag.parent

    sql = "INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?)"
    db.execute(sql, (name, entry_type, output_path))

    # Make directory for entries in this module
    Path(DESTINATION_DOCUMENT_BASE_DIR + "/" + output_dir).mkdir(parents=True, exist_ok=True)

    # Find entry links
    entries = module_section.xpath("ul/li/a")
    for entry in entries:
        entry_url = entry.attrib.get("href")
        if not entry_url:
            continue

        entry_title = entry.attrib.get("title")
        entry_file = entry_url.split("#")[0]
        entry_filename = entry_file.split("/")[-1]
        entry_path = f"{SOURCE_DOCUMENT_BASE_DIR}/api/{entry_file}"
        entry_output_path = f"{output_dir}/{entry_filename}"

        entry_soup = BeautifulSoup(open(entry_path, "r").read(), "html.parser")
        entry_type = entry_soup.title.text.split()[0]

        clean_article(entry_soup)

        # Write the results
        entry_output_file = open(f"{DESTINATION_DOCUMENT_BASE_DIR}/{entry_output_path}", "w")
        entry_output_file.write(str(entry_soup))
        entry_output_file.close
        logger.info(f"Wrote to {DESTINATION_DOCUMENT_BASE_DIR}/{entry_output_path}")

        sql = "INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?)"
        db.execute(sql, (name + "/" + entry_title, entry_type, output_dir + "/" + entry_filename))

    output_file = open(f"{DESTINATION_DOCUMENT_BASE_DIR}/{output_path}", "w")
    output_file.write(str(soup))
    output_file.close()

    logger.info(f"Wrote to {DESTINATION_DOCUMENT_BASE_DIR}/{output_path}")

db.commit()
