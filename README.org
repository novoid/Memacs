*What were you doing* on February 14th of 2007? On *which tasks* were
you working on that very day you met your girl friend? When was the
*last appointments* with your dentist? *Who called* you on telephone
during that meeting with your customer last month?

Most people can not answer such questions. *With Memacs you can!*

Memacs extracts metadata (subjects, timestamps, contact information,
...) from many different existing data sources (file names, emails,
tweets, bookmarks, ...) on your computer and generates files which are
readable by [[http://en.wikipedia.org/wiki/Emacs][GNU Emacs]] with [[http://orgmode.org/][Org mode]].

Example:
:    emails              -> memacs-maildir.py  \
:    firefox history     -> memacs-firefox.py   |
:    SMS                 -> memacs-sms.py       |
:    RSS-feeds           -> memacs_rss.py       |
:    bank statements     -> memacs-easybank.py  |>  Memacs
:    postings            -> memacs-slrn.org     |
:    git repository logs -> memacs_git.py       |
:    svn repository logs -> memacs_svn.py      /
:    |_________________|   |_________________|     |______|
:    your personal data      Memacs modules        Org mode

Memacs - as the central component of the system - is a hub for all the
connectors that add data from individual data sources. Those connectors
are called *Memacs modules* or short /module/.

Your agenda automatically gets populated with entries similar to the example shown in the screenshot from [[http://arxiv.org/abs/1304.1332][the white paper]]:

[[file:https://github.com/novoid/screencasts/raw/master/memacs/2012-04-08_Memacs_2008-09-15_archive.png]]

You can see some demo data using the modulees for SMS, filenamedatestamps, Twitter, RSS, imap, phonecalls, and git.

- *target group*: Users of  [[http://en.wikipedia.org/wiki/Emacs][Emacs]] and [[http://orgmode.org/][Org mode]]
- *skills necessary*: creating/modifying shell script code; creating
  scheduled tasks
- *project hosted on* https://github.com/novoid/Memacs


** Table of Contents
- [[#installation][Installation]]
- [[#getting-started][Getting started]]
- [[#workflows][Workflows]]
- [[#memacs-modules][Memacs modules]]
- [[#changelog][Changelog]]
- [[#example-story][Example story]]
- [[#background][Background]]
- [[#contribute][Contribute]]
- [[#license][License]]

** Installation

*** Install using Pip

The easiest way of installing Memacs is by using `pip`:

: pip install memacs[all]

This gets you the whole set of modules with all dependencies on your system.

If you would like to define the dependencies more fine-grained, you
can use one or more of the extras: =gps=, =rss=, =ical=, =lastfm=,
=battery=, or =twitter= like the following example:

: pip install memacs[gps,rss]

*** Manual Setup from Git

In case you prefer to set the environment "the old way", you can do it manually:

- clone or download repository from github
- make sure to use *Python version 3*
- create a virtualenv or
- export/set ~PYTHONPATH~

: PYTHONPATH=/path/to/memacs

- install dependencies

: pip install -r requirements.txt

** Getting Started

The basic concept of using a Memacs module is following:

1. Choose a Memacs module you want to use and set it up:
   - Read the module descripion files in the ~docs~ folder.
   - Each [[#memacs-modules][module]] shares global options but also comes with its very
     own set of custom arguments.
   - Manually start the module of your choice from the ~bin~ folder of
     Memacs with the argument ~--help~, e.g. ~bin/memacs_csv.py
     --help~ in your command line in order to get an overview of the
     arguments of this module.
   - You probably want to *develop and test a script (=.bat= or =.sh=)
     for the module invocation* in the command line and ...
2. When this script works as expected, set up a periodical invocation
   so that your data gets converted to Org mode via Memacs regularily.
   - This is usually done via operating system dependent methods:
     - Windows: [[https://docs.microsoft.com/en-us/windows/desktop/taskschd/task-scheduler-start-page][Task Scheduler]]
     - GNU/Linux: [[https://en.wikipedia.org/wiki/Cron][cron job]] or via [[https://wiki.archlinux.org/index.php/Systemd/Timers][systemd]]
     - macOS: [[http://www.launchd.info/][launchd]]
3. For an update from a running instance of Emacs, independent of a
   recurrent schedule (e.g., Memacs' photo module after returning from
   an excursion), you may add a key binding to Emacs, e.g. =C-c m p=
   to your configuration

   #+begin_src emacs-lisp
     (defun mp-update-memacs-photos ()
       "An extra (i.e., not cron-scheduled) run of Memacs' photo module."
       (interactive)
	 (shell-command
	   (format "~/org/update-memacs-photos.sh")
	 )
     )

     (global-set-key (kbd "C-c m p") 'mp-update-memacs-photos)
   #+end_src

   The script called requires the provision of the executable bit.
   Additional background of this technique is compiled by Mickey
   Petersen in [[https://www.masteringemacs.org/article/mastering-key-bindings-emacs][Mastering Key Bindings in Emacs]].
4. Think of another Memacs module you might want to try ;-)

Please make sure you also read the [[docs/FAQs_and_Best_Practices.org][FAQ's and best practices]], as it
contains many tips and tricks on how to meet your requirements and on
how to choose a reasonable setup.

** Workflows

Here are some workflows just to give you an initial impression how
Memacs may give you much for digital fun.

*** The Basics

When one or more Memacs modules are set-up and data starts flowing in
to your Memacs Org mode files, you have many options to use Memacs for
your personal workflows.

The most basic thing that changes with Memacs is that you might want
to see Memacs-processed data in your agenda:

Either you are generating (1) Org mode files that are within your
[[https://orgmode.org/manual/Agenda-files.html][agenda files]] or you are generating (2) [[https://orgmode.org/manual/Archiving.html#Archiving][archive files]] whose more or
less empty Org mode file stub is within your agenda files (as
described in the [[https://github.com/novoid/Memacs/blob/master/docs/FAQs_and_Best_Practices.org#performance-and-scalability][FAQs]]).

This way, the generated time-stamp information gets into your normal
agenda (1) or in the [[https://orgmode.org/manual/Agenda-commands.html][extended in archives-mode]] (by pressing =v A= in
your agenda) that also shows content of the archive files (2).

*** Filename Time-Stamp and Friends

A Memacs feature I personally use all the time provides a somewhat
more complex workflow whose basic data is provided by the [[docs/memacs_filenametimestamps.org][filename
time-stamp module]]. The module indexes all my files that contain
ISO-datestamps or ISO-timestamps in their file names just like
[[http://linux-sxs.org/utilities/updatedb.html][updatedb]] does for "locate".

The fun starts, when this module is set-up and the file index is
generated (nightly). With the elisp snippets mentioned in the module
documentation, I am able to link to any of those files just by
specifying their file name. This links never get broken since it does
not matter in which folder files are located in any more.

Please refer to [[https://github.com/novoid/dot-emacs/blob/master/config.org#handling-tsfile-links-memacs][my Emacs configuration]] and look out for all
occurrences of =tsfile= (time-stamp file) which is my custom link for
those files.

I even extended this workflow such that my [[https://github.com/novoid/lazyblorg][blog system]] is able to [[https://github.com/novoid/lazyblorg/wiki/Images#embedding-tsfile-image-files][link
to =tsfile:= images]] independent of their location. Awesome stuff.

** Memacs Modules

- [[docs/memacs_arbtt.org][arbtt]]
- [[docs/memacs_battery.org][battery]]
- [[docs/memacs_csv.org][csv]]
- [[docs/memacs_filenametimestamps.org][filenametimestamps]]
- [[file:docs/memacs_firefox_history.org][firefox_history]]
- [[file:docs/memacs_chrome_history.org][chrome_history]]
- [[docs/memacs_git.org][git]]
- [[docs/memacs_gpx.org][gpx]]
- [[docs/memacs_ical.org][ical]]
- [[docs/memacs_imap.org][imap]]
- [[docs/memacs_lastfm.org][lastfm]]
- [[docs/memacs_mumail.org][mu]]
- [[docs/memacs_phonecalls.org][phonecalls]]
- [[docs/memacs_photos.org][photos]]
- [[docs/memacs_rss.org][rss]]
- [[docs/memacs_simplephonelogs.org][simplephonelogs]]
- [[docs/memacs_sms.org][sms]]
- [[docs/memacs_svn.org][svn]]
- [[docs/memacs_twitter.org][twitter]]
- [[docs/memacs_whatsapp.org][whatsapp]]
- [[docs/memacs_kodi.org][KODI logs]]

This module is an example for developers: [[docs/memacs_csv.org]]

Those modules are *not* adopted to the new unified framework yet:

- [[tmp/emails/maildir/memacs-maildir.org][maildir]]
- [[tmp/emails/mbox/memacs-mbox.org][mbox]] (also useful for newsgroups)
  - see also [[tmp/emails/mbox/works-for-me-hack/memacs-mbox.org]]

- *bank account*:
  - [[http://www.easybank.at][easybank.at]]: see [[tmp/bank_statements/easybank.at/memacs-easybank.org]]

- *newsgroups*
  - *[[http://en.wikipedia.org/wiki/Slrn][slrn]]*: see [[tmp/emails/mbox/works-for-me-hack/memacs-mbox.org]]

Following modules exist as a rough idea only and might get implemented
some day (by you?):

- *[[http://karl-voit.at/tagstore/][tagstore]]*: see [[tmp/tagstore/memacs-tagstore.org]]

- *calendar*:
  - [[http://www.jpilot.org/][JPilot]]-datebook: see [[tmp/calendars/memacs-jpilot-datebook.org]]

- *tasks*:
  - [[http://www.jpilot.org/][JPilot]]-todos: see [[tmp/tasklists/jpilot-todos/memacs-jpilot-todos.org]]

- *blog_systems*:
  - [[http://en.wikipedia.org/wiki/Serendipity_(weblog_software)][Serendipity]]: see [[tmp/blog_systems/serendipity/memacs-serendipity.org]]

** Changelog

- Version 2020.06.05.1
  - Features
    - New module: [[https://github.com/novoid/Memacs/blob/master/docs/memacs_kodi.org][memacs_kodi]]
    - Andrea Ghensi [[https://github.com/novoid/Memacs/pull/100][provided an improved pip setup method]]
  - Bugfixes
    - fix chrome.py output to include url and title for org headings
    - many improvements for the Chrome module
    - filenametimestamps: fixed check_datestamp_correctness ([[https://github.com/novoid/Memacs/issues/97][#97]])

- Version 2019.11.06.1
  - Features
    - [[https://github.com/novoid/orgformat][orgformat is now an external library]]
  - Bugfixes
    - Fix problems when locale is not en_US

- Versions prior to 2019-10-09.1 are not documented using this
  changelog. Please read the git commit messages.

* Example Story

Imagine you are already using Memacs.

When remembering that day, when you joined an interesting talk about
«[[http://en.wikipedia.org/wiki/Getting_Things_Done][Getting Things Done]]» (GTD), you start up your GNU Emacs with your main
Org mode file. There you go to the Agenda-view and select this
specific day a couple of months ago.

There it is, from 2pm to 3pm you scheduled this talk in your calendar.
And then you realize that within this time frame, there appear some
[[http://en.wikipedia.org/wiki/Jpeg][JPEG files]] containing an [[http://www.cl.cam.ac.uk/~mgk25/iso-time.html][ISO 8601]] time stamp[1] are indexed by one
module. (filenametimestamp-module)

This image contains a slide you found interesting and which you
photographed using your sleek smartphone. Who would remember having
taken a picture during a talk?

Ten minutes after the talk you wrote a short message on [[http://Twitter.com][Twitter]] where
you mentioned useful URLs for your followers. This time those URLs are
handy for yourself too! (Twitter-module)

On the evening of that day you see an entry of an incoming email from
the author of the talk. Now you remember having had a cool
conversation at the end of the talk where he promised you some
additional information about that nice little GTD tool on his
computer. Great that you got that link to that email too. Without
Memacs you would probably never remembered that email again.
(Maildir-module)

And then there were some bookmarks you saved this day, almost all
related to great ideas you got from the GTD talk. (delicious-module)

This small story shows only a few use cases where different modules
combine given data sources and their information to provide an overall
view related to an event. Since Org mode has got links, no actual data
has to be duplicated (except the meta data extracted by Memacs).
Emails, files, bookmarks, and so forth are linked rather than copied.

[1] with periods instead of colons - just because the [[http://msdn.microsoft.com/en-us/library/aa365247(v%3Dvs.85).aspx#naming_conventions][ancient
limitations of Microsoft based file systems]]; like «2011-02-14T14.35.42
ideas.jpg»

* Background

In 1945, [[http://en.wikipedia.org/wiki/Vannevar_Bush][Vannevar Bush]] wrote a famous article «[[http://en.wikipedia.org/wiki/As_We_May_Think][As We May Think]]» where
he develops the idea of having a «memory extender» called *Memex*. The
memex can store all letters, books, and other information which are
related to a person.

Besides having foreseen several technologies like hypertext, he
defined a device that holds all metadata and data and provides
associative trails to access information.

In the last decade of the previous century Microsoft Research had a
research program that resulted in [[http://en.wikipedia.org/wiki/MyLifeBits][MyLifeBits]]. This software tried to
store each information of the user like office documents, screenshots,
name of active windows on the desktop computer, and even automatically
took photographs ([[http://en.wikipedia.org/wiki/Sensecam][SenseCam]]). This word did not result in any (open)
software product. Bell and Gemmell wrote a book called «[[http://www.amazon.de/gp/product/0525951342/ref%3Das_li_ss_tl?ie%3DUTF8&tag%3Dkarlssuder-21&linkCode%3Das2&camp%3D1638&creative%3D19454&creativeASIN%3D0525951342][Total Recall]]».

The Memacs project tries to implement the ideas of Vannevar Bush's
vision with open source and open standards. Hence, it's name «Memacs»
is the obvious combination of «[[http://www.gnu.org/software/emacs/][GNU Emacs]]» and «Memex».

Memacs uses GNU Emacs Org mode to visualize and access information
extracted by Memacs modules: using tags, time stamps, full text
search, and so forth GNU Emacs is able to derive different
views. The most important view probably is the [[http://orgmode.org/org.html#Agenda-Views][Agenda-view]] where you
can see anything that happened during a specific day/week/month
according to the time frame selected. But you can derive other views
too. For example you can choose to generate a condensed search result
using a [[http://en.wikipedia.org/wiki/Boolean_algebra_(logic)][boolean combination]] of tags.

Related to Memacs, the project founder developed a research software
called *[[http://karl-voit.at/tagstore/][tagstore]]*. This system allows users to store (local) files
using tags without a hierarchy of folders. As a natural extension,
tagstore targets associative access for (local) files. You might want
to check out tagstore too. Memacs and tagstore are a very useful
combination.

If you do like to know how to efficiently organize digital files in a
simple and operating system independent way, read [[http://karl-voit.at/managing-digital-photographs/][this blog post]] from
Karl. It might give you ideas for your workflows as well.

Karl also wrote [[http://arxiv.org/abs/1304.1332][a whitepaper on Memacs]] which describes Memacs from a
scientists point of view.

* Similar Projects

- In https://github.com/novoid/Memacs/issues/88, Alex links to a
  browser extension from [[https://worldbrain.io/][WorldBrain]] called [[https://github.com/WorldBrain/Memex][Memex]].
- https://github.com/karlicoss/orger has similar goals: converting
  data into Org mode

* Contribute! We are looking for your ideas:

If you want to contribute to this cool project, please fork and
contribute or write an additional module!

See [[docs/FAQs_and_Best_Practices.org]] for more developing information.

We are sure that there are a *lot* of cool ideas for other modules out
there! This is just the beginning!

Memacs is designed with respect to minimal effort for new modules.

We are using [[http://www.python.org/dev/peps/pep-0008/][Python PEP8]] and [[http://en.wikipedia.org/wiki/Test-driven_development][Test Driven Development (TDD)]].

* License

Memacs is licensed under the GPLv3 [[license.txt][license]].
