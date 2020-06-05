from setuptools import setup, find_packages

# building extra requirements with "all" option to install everything at once
extras_require = {
    "gps": ["gpxpy", "geocoder"],
    "rss": ["feedparser"],
    "ical": ["icalendar"],
    "lastfm": ["pylast"],
    "battery": ["batinfo"],
    "twitter": ["python-dateutil", "twython"],
}
extras_require["all"] = {r for v in extras_require.values() for r in v}

setup(
    name="memacs",
    version="2020.06.05.1",
    description="Visualize your (digital) life in Emacs Org mode "
                "by converting data to Org mode format",
    author="Karl Voit",
    author_email="tools@Karl-Voit.at",
    url="https://github.com/novoid/memacs",
    download_url="https://github.com/novoid/memacs/zipball/master",
    keywords=["quantified self", "emacs", "org-mode", "org mode"],
    packages=find_packages(),  # Required
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
    # package_data={},
    install_requires=["orgformat", "emoji"],
    extras_require=extras_require,
    entry_points={
        'console_scripts': [
            "memacs_arbtt=bin.memacs_arbtt:main",
            "memacs_battery=bin.memacs_battery:main [battery]",
            "memacs_chrome=bin.memacs_chrome:main",
            "memacs_csv=bin.memacs_csv:main",
            "memacs_example=bin.memacs_example:main",
            "memacs_filenametimestamps=bin.memacs_filenametimestamps:main",
            "memacs_firefox=bin.memacs_firefox:main",
            "memacs_git=bin.memacs_git:main",
            "memacs_gpx=bin.memacs_gpx:main [gps]",
            "memacs_ical=bin.memacs_ical:main [ical]",
            "memacs_imap=bin.memacs_imap:main",
            "memacs_kodi=bin.memacs_kodi:main",
            "memacs_lastfm=bin.memacs_lastfm:main [lastfm]",
            "memacs_mumail=bin.memacs_mumail:main",
            "memacs_phonecalls=bin.memacs_phonecalls:main",
            "memacs_phonecalls_superbackup=bin.memacs_phonecalls_superbackup:main",
            "memacs_photos=bin.memacs_photos:main",
            "memacs_rss=bin.memacs_rss:main [rss]",
            "memacs_simplephonelogs=bin.memacs_simplephonelogs:main",
            "memacs_sms=bin.memacs_sms:main",
            "memacs_sms_superbackup=bin.memacs_sms_superbackup:main",
            "memacs_svn=bin.memacs_svn:main",
            "memacs_twitter=bin.memacs_twitter:main [twitter]",
            "memacs_whatsapp=bin.memacs_whatsapp:main",
        ],
     },
    long_description="""This Python framework converts data from various sources to Org mode format
which may then included in Org mode agenda (calendar). This way, you get a 360-degree-view of your
digital life.

Each Memacs module converts a different input format into Org mode files.

- Target group: users of Emacs Org mode who are able to use command line tools
- Hosted and documented on github: https://github.com/novoid/memacs
"""
)
