#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from memacs.podcastaddict import PodcastAddict

PROG_VERSION_NUMBER = "0.1"
PROG_VERSION_DATE = "2026-05-25"
PROG_SHORT_DESCRIPTION = "Memacs for PodcastAddict backups"
PROG_TAG = "podcast"
PROG_DESCRIPTION = """
This Memacs module reads the most recent
PodcastAddict_autoBackup_*.backup file from a user-supplied directory
and emits one Org-mode entry per finished podcast episode
(seen_status = 1).

Each backup file is a ZIP archive that contains the
podcastAddict.db SQLite database. Episodes are joined to their
podcasts via podcast_id; the entry's time-stamp is the episode's
playbackDate converted to local time.
"""

COPYRIGHT_YEAR = "2026"
COPYRIGHT_AUTHORS = "Karl Voit <tools@Karl-Voit.at>"


def main():
    memacs = PodcastAddict(
        prog_version=PROG_VERSION_NUMBER,
        prog_version_date=PROG_VERSION_DATE,
        prog_description=PROG_DESCRIPTION,
        prog_short_description=PROG_SHORT_DESCRIPTION,
        prog_tag=PROG_TAG,
        copyright_year=COPYRIGHT_YEAR,
        copyright_authors=COPYRIGHT_AUTHORS,
    )
    memacs.handle_main()


if __name__ == "__main__":
    main()
