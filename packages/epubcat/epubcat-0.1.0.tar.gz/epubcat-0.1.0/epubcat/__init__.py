# SPDX-FileCopyrightText: 2024-present root <root@localhost>
#
# SPDX-License-Identifier: MIT
import logging
import logging.config
from pathlib import Path

from ebooklib import epub
from lxml.html import fromstring as lxfstr
import ftfy


logging.config.dictConfig({"version":1,"handlers": {"default": {"level":"INFO", 'class':"logging.StreamHandler", 'stream':'ext://sys.stdout'}}})

def cat_epub(path: Path):
    if not path.exists() or not path.is_file():
        logging.fatal(f"Path {path} is not found or is not a file. Exiting")
        raise SystemExit(1)
    file = epub.read_epub(path)
    for page in file.get_items_of_media_type('application/xhtml+xml'):
        try:
            page_doc = lxfstr(page.get_body_content())
            page_text = page_doc.text_content()
            for line in filter(None,map(str.strip, page_text.split('\r\n'))):
                yield ftfy.fix_text(line)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as exc:
            logging.warning(f"Exception occurred: {exc}. Continuing")
            continue
