#!/usr/bin/env python3
"""Fetch and update appjk recommendation JSON files with recent hot data."""

import argparse
import html
import json
import os
import re
import time
import urllib.error
import urllib.request

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

SOURCES = {
    "novel": "https://book.douban.com/chart",
    "music": "https://music.douban.com/chart",
    "comic": "https://book.douban.com/tag/%E6%BC%AB%E7%94%BB?start=0&type=T",
    "movie": "https://movie.douban.com/chart",
}


def fetch_text(url: str, timeout: int = 20, retries: int = 3) -> str:
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                raw = response.read()
                return raw.decode("utf-8", errors="replace")
        except urllib.error.URLError as err:
            if attempt == retries:
                raise
            time.sleep(1)
    raise RuntimeError("Unable to fetch URL: %s" % url)


def clean_text(value: str) -> str:
    if value is None:
        return ""
    return html.unescape(re.sub(r"\s+", " ", value)).strip()


def parse_douban_novel(html_text: str, limit: int = 12) -> list[dict]:
    blocks = re.findall(r'<li\s+class="media clearfix">(.*?)</li>', html_text, re.S)
    items = []
    for index, block in enumerate(blocks[:limit], start=1):
        title_match = re.search(r'<h2[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block, re.S)
        pic_match = re.search(r'<img[^>]*src="([^"]+)"', block, re.S)
        update_match = re.search(r'<p[^>]*class="subject-abstract[^"]*"[^>]*>(.*?)</p>', block, re.S)
        if not title_match:
            continue
        url = clean_text(title_match.group(1))
        name = clean_text(title_match.group(2))
        pic = clean_text(pic_match.group(1)) if pic_match else ""
        update_time = clean_text(update_match.group(1)) if update_match else ""
        item_id = f"novel_{index}"
        items.append(
            {
                "id": item_id,
                "name": name,
                "pic": pic,
                "updateTime": update_time,
                "contentUrl": url,
            }
        )
    return items


def parse_douban_music(html_text: str, limit: int = 12) -> list[dict]:
    pattern = re.compile(
        r'<li class="clearfix">.*?<span class="rank">(\d+)</span>.*?<p class="entry">.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>\s*&nbsp;/&nbsp;(.*?)</p>.*?<span class="days">(.*?)</span>',
        re.S,
    )
    items = []
    for index, match in enumerate(pattern.findall(html_text), start=1):
        if index > limit:
            break
        rank, url, name, author, days = match
        name = clean_text(name)
        author = clean_text(author)
        days = clean_text(days)
        item_id = f"music_{index}"
        items.append(
            {
                "id": item_id,
                "name": f"{name} - {author}" if author else name,
                "pic": "",
                "updateTime": days,
                "contentUrl": url,
            }
        )
    if not items:
        # fallback for other music list structures
        simple = re.findall(r'<a[^>]*href="(https://music.douban.com/subject/[^"]+)"[^>]*>([^<]+)</a>\s*&nbsp;/&nbsp;([^<]+)', html_text)
        for index, match in enumerate(simple[:limit], start=1):
            url, name, author = match
            items.append(
                {
                    "id": f"music_{index}",
                    "name": clean_text(name),
                    "pic": "",
                    "updateTime": "",
                    "contentUrl": clean_text(url),
                }
            )
    return items


def parse_douban_comic(html_text: str, limit: int = 12) -> list[dict]:
    blocks = re.findall(r'<li class="subject-item">(.*?)</li>', html_text, re.S)
    items = []
    for index, block in enumerate(blocks[:limit], start=1):
        url_match = re.search(r'<a[^>]*href="([^"]+)"[^>]*>', block)
        title_match = re.search(r'<h2[^>]*>.*?<a[^>]*title="([^"]+)"[^>]*>', block, re.S)
        if not title_match or not url_match:
            title_match = re.search(r'<h2[^>]*>.*?<a[^>]*>(.*?)</a>', block, re.S)
        pic_match = re.search(r'<img[^>]*src="([^"]+)"', block)
        url = clean_text(url_match.group(1))
        name = clean_text(title_match.group(1) if title_match else "")
        pic = clean_text(pic_match.group(1)) if pic_match else ""
        item_id = f"comic_{index}"
        items.append(
            {
                "id": item_id,
                "name": name,
                "pic": pic,
                "updateTime": "",
                "contentUrl": url,
            }
        )
    return items


def parse_douban_movie(html_text: str, limit: int = 12) -> list[dict]:
    blocks = re.findall(r'<tr class="item">(.*?)</tr>', html_text, re.S)
    items = []
    for index, block in enumerate(blocks[:limit], start=1):
        link_match = re.search(r'<a[^>]*class="nbg"[^>]*href="([^"]+)"[^>]*title="([^"]+)"', block, re.S)
        img_match = re.search(r'<img[^>]*src="([^"]+)"', block, re.S)
        title_match = re.search(r'<div class="pl2">.*?<a[^>]*href="[^"]+"[^>]*>(.*?)</a>', block, re.S)
        year_match = re.search(r'<p>(.*?)</p>', block, re.S)
        if not link_match:
            continue
        url = clean_text(link_match.group(1))
        name = clean_text(link_match.group(2) if link_match.group(2) else (title_match.group(1) if title_match else ""))
        pic = clean_text(img_match.group(1)) if img_match else ""
        year = clean_text(year_match.group(1)) if year_match else ""
        year_found = re.search(r'(\d{4})', year)
        year_value = year_found.group(1) if year_found else ""
        items.append(
            {
                "vod_id": f"movie_{index}",
                "vod_name": name,
                "vod_pic": pic,
                "vod_year": year_value,
                "vod_play_url": f"详情${url}",
            }
        )
    return items


def write_json(path: str, data: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump({"list": data}, handle, ensure_ascii=False, indent=4)


def run_update(categories: list[str], limit: int = 12, base_dir: str | None = None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    results = {}
    for category in categories:
        source_url = SOURCES.get(category)
        if source_url is None:
            raise ValueError(f"Unknown category: {category}")
        print(f"Fetching {category} from {source_url}...")
        html_text = fetch_text(source_url)
        if category == "novel":
            results[category] = parse_douban_novel(html_text, limit)
        elif category == "music":
            results[category] = parse_douban_music(html_text, limit)
        elif category == "comic":
            results[category] = parse_douban_comic(html_text, limit)
        elif category == "movie":
            results[category] = parse_douban_movie(html_text, limit)
        else:
            results[category] = []
        print(f"Parsed {len(results[category])} items for {category}.")

    writes = {
        "novel": "novelRecommend.json",
        "music": "musicRecommend.json",
        "comic": "comicRecommend.json",
        "movie": "movieRecommend.json",
    }
    for category, items in results.items():
        if not items:
            print(f"Warning: no items parsed for {category}, skipping file write.")
            continue
        output_path = os.path.join(base_dir, writes[category])
        write_json(output_path, items)
        print(f"Wrote {len(items)} items to {output_path}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update appjk recommend JSON files with latest hot data.")
    parser.add_argument(
        "--categories",
        nargs="+",
        choices=["novel", "music", "comic", "movie"],
        default=["novel", "music", "comic", "movie"],
        help="Categories to update.",
    )
    parser.add_argument("--limit", type=int, default=12, help="Maximum number of items per category.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_update(args.categories, args.limit)


if __name__ == "__main__":
    main()
