from distutils.core import setup
import glob

setup(
    name = "memacs",
    packages = ["bin","memacs","memacs/lib", "memacs/lib/tests", "memacs/tests"],
    version = "0.0.13",
    description = "Memacs extracts metadata from many different existing data sources on your computer and generates files which are readable by GNU Emacs(Org-Mode).",
    author = "Karl Voit",
    author_email = "tools@Karl-Voit.at",
    url = "https://github.com/novoid/Memacs",
    download_url = "https://github.com/novoid/Memacs/zipball/master",
    keywords = ["org-mode", "org"],
    scripts = glob.glob("bin/memacs_*"),
    install_requires = ["PIL","icalendar","feedparser"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        ],
    long_description = """\
Memacs
-----------------------------
*What were you doing* on February 14th of 2007? On *which tasks* were
you working on that very day you met your girl friend? When was the
*last appointments* with your dentist? *Who called* you on telephone
during that meeting with your customer last month?

Most people can not answer such questions. *With Memacs you can!*

Memacs extracts metadata (subjects, timestamps, contact information,
...) from many different existing data sources (file names, emails,
tweets, bookmarks, ...) on your computer and generates files which are
readable by GNU Emacs with Org-mode.    
"""
)