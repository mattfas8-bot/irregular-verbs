#!/usr/bin/env python3
"""
Pull the top-5 YouTube results for a set of queries under the
"This month" + "4-20 minutes" filters and print

    title | views | channel | subscribers | upload date

plus the views/subscribers ratio per video and per query group.

Two backends, pick whichever you can run:

  API    (exact, fast, needs a free YouTube Data API v3 key)
         YT_API_KEY=... python3 scripts/yt_scan.py --backend api

  yt-dlp (no key, scrapes the same filtered search page)
         pip install -U yt-dlp
         python3 scripts/yt_scan.py --backend ytdlp

Both honour the same two filters:
  * upload date = last 30 days ("This month")
  * duration    = 4-20 minutes ("Medium" / videoDuration=medium)
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

# sp= payload for the YouTube results page: upload_date=month, type=video,
# duration=medium(4-20min). Protobuf {2:{1:4, 2:1, 3:3}} base64'd.
SP_MONTH_VIDEO_MEDIUM = "EgYIBBABGAM%3D"

GROUPS: dict[str, list[str]] = {
    "space/physics": [
        "how black holes actually work",
        "what happens inside a neutron star",
        "why time slows down explained",
    ],
    "ai news": [
        "AI news this week",
        "biggest AI news",
    ],
}

TOP_N = 5
API = "https://www.googleapis.com/youtube/v3"


# --------------------------------------------------------------------------
# backend: YouTube Data API v3
# --------------------------------------------------------------------------
def _api(endpoint: str, key: str, **params) -> dict:
    params["key"] = key
    url = f"{API}/{endpoint}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)


def fetch_api(query: str, key: str) -> list[dict]:
    published_after = (
        datetime.now(timezone.utc) - timedelta(days=30)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")

    search = _api(
        "search",
        key,
        part="snippet",
        q=query,
        type="video",
        videoDuration="medium",       # 4-20 minutes
        publishedAfter=published_after,  # "this month"
        order="relevance",
        maxResults=TOP_N,
    )
    video_ids = [item["id"]["videoId"] for item in search.get("items", [])]
    if not video_ids:
        return []

    videos = _api("videos", key, part="snippet,statistics", id=",".join(video_ids))
    channel_ids = {v["snippet"]["channelId"] for v in videos["items"]}
    channels = _api("channels", key, part="statistics", id=",".join(channel_ids))
    subs = {
        c["id"]: int(c["statistics"].get("subscriberCount", 0))
        for c in channels["items"]
    }

    order = {vid: i for i, vid in enumerate(video_ids)}
    rows = [
        {
            "title": v["snippet"]["title"],
            "views": int(v["statistics"].get("viewCount", 0)),
            "channel": v["snippet"]["channelTitle"],
            "subs": subs.get(v["snippet"]["channelId"], 0),
            "date": v["snippet"]["publishedAt"][:10],
        }
        for v in sorted(videos["items"], key=lambda v: order[v["id"]])
    ]
    return rows


# --------------------------------------------------------------------------
# backend: yt-dlp
# --------------------------------------------------------------------------
def _ytdlp(args: list[str]) -> dict:
    out = subprocess.run(
        ["yt-dlp", "-J", "--no-warnings", *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(out.stdout)


def fetch_ytdlp(query: str, _key: str | None = None) -> list[dict]:
    url = (
        "https://www.youtube.com/results?search_query="
        + urllib.parse.quote_plus(query)
        + "&sp="
        + SP_MONTH_VIDEO_MEDIUM
    )
    search = _ytdlp(["--flat-playlist", "--playlist-end", str(TOP_N), url])

    rows = []
    for entry in search.get("entries", [])[:TOP_N]:
        # the flat listing has no subscriber count or exact date, so pull the
        # watch page for each hit
        info = _ytdlp(["--skip-download", f"https://www.youtube.com/watch?v={entry['id']}"])
        upload = info.get("upload_date") or ""
        rows.append(
            {
                "title": info.get("title", entry.get("title", "")),
                "views": info.get("view_count") or 0,
                "channel": info.get("channel") or info.get("uploader") or "",
                "subs": info.get("channel_follower_count") or 0,
                "date": f"{upload[:4]}-{upload[4:6]}-{upload[6:]}" if upload else "?",
            }
        )
    return rows


# --------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------
def ratio(row: dict) -> float | None:
    return row["views"] / row["subs"] if row["subs"] else None


def print_query(query: str, rows: list[dict]) -> None:
    print(f"\n### {query}")
    if not rows:
        print("(no results under the filters)")
        return
    print("название | просмотры | канал | подписчики | дата загрузки | views/subs")
    for r in rows:
        rr = ratio(r)
        subs = f"{r['subs']:,}" if r["subs"] else "n/a"
        rel = f"{rr:.2f}" if rr is not None else "n/a"
        print(
            f"{r['title']} | {r['views']:,} | {r['channel']} | "
            f"{subs} | {r['date']} | {rel}"
        )


def summarize(group: str, rows: list[dict]) -> None:
    ratios = [r for r in (ratio(x) for x in rows) if r is not None]
    if not ratios:
        print(f"\n{group}: no ratio data")
        return
    print(
        f"\n{group}: n={len(ratios)} | median views/subs={statistics.median(ratios):.2f} "
        f"| mean={statistics.fmean(ratios):.2f} | max={max(ratios):.2f} "
        f"| median views={statistics.median(r['views'] for r in rows):,.0f}"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=["api", "ytdlp"], default="ytdlp")
    ap.add_argument("--json", action="store_true", help="also dump raw rows as JSON")
    args = ap.parse_args()

    key = os.environ.get("YT_API_KEY", "")
    if args.backend == "api" and not key:
        print("set YT_API_KEY (YouTube Data API v3) or use --backend ytdlp", file=sys.stderr)
        return 2
    fetch = fetch_api if args.backend == "api" else fetch_ytdlp

    everything: dict[str, list[dict]] = {}
    for group, queries in GROUPS.items():
        print(f"\n{'=' * 70}\n{group.upper()}\n{'=' * 70}")
        group_rows: list[dict] = []
        for query in queries:
            rows = fetch(query, key)
            everything[query] = rows
            group_rows += rows
            print_query(query, rows)
        summarize(group, group_rows)

    if args.json:
        print("\n" + json.dumps(everything, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
