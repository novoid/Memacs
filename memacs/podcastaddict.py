#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import json
import logging
import os
import re
import sqlite3
import sys
import tempfile
import time
import zipfile

import pypandoc
from orgformat import OrgFormat

from memacs.lib.memacs import Memacs
from memacs.lib.orgproperty import OrgProperties


DB_NAME = "podcastAddict.db"


class PodcastAddict(Memacs):
    def _parser_add_arguments(self):
        Memacs._parser_add_arguments(self)
        self._parser.add_argument(
            "-d", "--backup-dir", dest="backup_dir", required=True,
            metavar="DIR",
            help="path to the directory containing "
                 "PodcastAddict_autoBackup_*.backup files; "
                 "the most recently modified .backup file is used")

    def _parser_parse_args(self):
        Memacs._parser_parse_args(self)
        if not os.path.isdir(self._args.backup_dir):
            self._parser.error(
                "backup directory does not exist: %s" % self._args.backup_dir)

    def _find_latest_backup(self):
        pattern = os.path.join(self._args.backup_dir, "*.backup")
        candidates = glob.glob(pattern)
        if not candidates:
            logging.error("no *.backup files found in %s", self._args.backup_dir)
            sys.exit(1)
        latest = max(candidates, key=os.path.getmtime)
        logging.info("using backup file: %s", latest)
        return latest

    def _extract_db(self, backup_path, tmpdir):
        with zipfile.ZipFile(backup_path) as zf:
            zf.extract(DB_NAME, tmpdir)
        return os.path.join(tmpdir, DB_NAME)

    def _main(self):
        backup_path = self._find_latest_backup()
        with tempfile.TemporaryDirectory(prefix="memacs_podcastaddict_") as tmpdir:
            db_path = self._extract_db(backup_path, tmpdir)
            # read-only URI so we never write back to the extracted copy
            conn = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True)
            conn.row_factory = sqlite3.Row
            try:
                self._emit_entries(conn)
            finally:
                conn.close()

    def _emit_entries(self, conn):
        cur = conn.cursor()
        cur.execute("""
            SELECT e._id           AS episode_id,
                   e.playbackDate  AS playback_date,
                   e.name          AS episode_name,
                   e.url           AS episode_url,
                   e.content       AS content,
                   e.duration      AS duration,
                   e.seasonNb      AS season_nb,
                   e.episodeNb     AS episode_nb,
                   e.transcript_url AS transcript_url,
                   p.name          AS podcast_name,
                   p.homepage      AS podcast_homepage
            FROM episodes e
            JOIN podcasts p ON e.podcast_id = p._id
            WHERE e.seen_status = 1 AND e.playbackDate > 0
            ORDER BY e.playbackDate
        """)
        count = 0
        for row in cur:
            self._write_entry(row)
            count += 1
        logging.info("wrote %d finished episodes", count)

    def _write_entry(self, row):
        ts_struct = time.localtime(row["playback_date"] / 1000.0)
        timestamp = OrgFormat.date(ts_struct, show_time=True)

        headline = self._build_headline(row)
        note = self._build_note(row)

        properties = OrgProperties(
            data_for_hashing="podcastaddict-{}-{}".format(
                row["episode_id"], row["playback_date"]))
        properties.add("PODCAST", row["podcast_name"] or "")
        if row["duration"]:
            properties.add("DURATION", row["duration"])
        if row["episode_url"]:
            properties.add("URL", row["episode_url"])

        self._writer.write_org_subitem(
            timestamp=timestamp,
            output=headline,
            note=note,
            properties=properties)

    def _build_headline(self, row):
        ep_link = _org_link(row["episode_url"], row["episode_name"])
        pod_link = _org_link(row["podcast_homepage"], row["podcast_name"])
        sxe = _format_season_episode(row["season_nb"], row["episode_nb"])
        suffix = " " + sxe if sxe else ""
        return "{ep} ({pod}{sfx})".format(ep=ep_link, pod=pod_link, sfx=suffix)

    def _build_note(self, row):
        parts = []
        transcript = _pick_transcript_url(row["transcript_url"])
        if transcript:
            parts.append("- [[{}][Transcript]]".format(transcript))
        if row["content"]:
            if parts:
                parts.append("")
            parts.append("Description:")
            parts.append("")
            parts.append(_html_to_org(row["content"]))
        return "\n".join(parts)


# --- helpers ---------------------------------------------------------------

def _org_link(url, text):
    text = (text or "").strip()
    url = (url or "").strip()
    if url and text:
        return "[[{}][{}]]".format(url, text)
    return text or url


def _format_season_episode(season, episode):
    # PodcastAddict uses -1 to mean "not set"; NULL is also possible.
    season = season if (season is not None and season > 0) else None
    episode = episode if (episode is not None and episode > 0) else None
    if season and episode:
        return "S{}E{}".format(season, episode)
    if episode:
        return "E{}".format(episode)
    if season:
        return "S{}".format(season)
    return ""


def _pick_transcript_url(transcript_json):
    if not transcript_json:
        return None
    try:
        data = json.loads(transcript_json)
    except (ValueError, TypeError):
        return None
    urls = data.get("urls") if isinstance(data, dict) else None
    if not urls:
        return None
    priority = {"srt": 0, "html": 1, "json": 2}
    best = min(urls, key=lambda u: priority.get(u.get("type"), 99))
    return best.get("url")


# PodcastAddict embeds in-app chapter-jump anchors like
# <a href="podcastaddict:195000">00:03:15</a>. Pandoc would faithfully
# render those as [[podcastaddict:195000][00:03:15]] Org links, which
# aren't useful outside the app, so strip them down to their text
# before handing the HTML to pandoc.
_RE_PA_LINK = re.compile(
    r'<a\b[^>]*href="podcastaddict:[^"]*"[^>]*>(.*?)</a>',
    re.DOTALL | re.IGNORECASE)

_PANDOC_ARGS = ["--wrap=none"]


def _html_to_org(content):
    cleaned = _RE_PA_LINK.sub(r"\1", content)
    org = pypandoc.convert_text(
        cleaned, to="org", format="html", extra_args=_PANDOC_ARGS)
    return org.strip()
