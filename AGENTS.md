# AGENTS.md

Guidance for AI coding agents working on Memacs.

## What this project is

Memacs is a Python 3 framework that converts data from many external sources
(emails, RSS, GPX, photos, phone calls, calendars, CSV files, ...) into
Org-mode files that can be consumed by Emacs + Org-mode (typically the
agenda). The repository contains:

1. **The framework** (`memacs/lib/`) — shared infrastructure: argument
   parsing, Org-mode output writing, property/ID handling, logging,
   readers.
2. **A collection of modules** (`memacs/<source>.py`) — one per data
   source. Each module subclasses `Memacs` and only implements the
   source-specific parsing logic.
3. **Thin entry-point scripts** (`bin/memacs_<source>.py`) — one per
   module. These only declare metadata (version, tag, description,
   copyright) and call `handle_main()`.
4. **Per-module user documentation** (`docs/memacs_<source>.org`).
5. **Unit tests** (`memacs/tests/` and `memacs/lib/tests/`).

The project is managed with [uv](https://docs.astral.sh/uv/);
`pyproject.toml` is the single source of truth for build, deps, and
console scripts. There is no `setup.py` / `requirements.txt`.

Many modules were contributed by peers, so style varies. The canonical
shape of a module is defined by the three example files referenced below.

## Required reading before adding or changing a module

Always study these together — they document the intended pattern:

- `bin/memacs_example.py` — entry-point template.
- `memacs/example.py` — module template (`Foo` subclass of `Memacs`).
- `memacs/tests/example_test.py` — test template using `test_get_entries()`.

When in doubt, compare against an existing module that already handles a
similar input:

- tabular: `memacs/csv.py`
- feed: `memacs/rss.py`
- SQLite-from-a-ZIP-backup + HTML shownotes: `memacs/podcastaddict.py`
- external CLI tool consumed via `subprocess`: `memacs/arbtt.py`
- file-tree walker: `memacs/filenametimestamps.py`

## The framework contract — what to reuse, what to write

The whole point of the framework is that a new module should focus on
*parsing the data source* and almost nothing else. Reuse, do not
re-invent.

### Reuse from `memacs.lib.memacs.Memacs` (the base class)

Subclass `Memacs` and override only these hooks:

- `_parser_add_arguments(self)` — call `Memacs._parser_add_arguments(self)`
  first, then add module-specific CLI arguments to `self._parser`.
- `_parser_parse_args(self)` — call `Memacs._parser_parse_args(self)`
  first, then post-process / validate `self._args`. Use
  `self._parser.error(...)` on bad input.
- `_main(self)` — the actual work. Read the input, parse it, and emit
  entries via `self._writer.write_org_subitem(...)`.

You get the following for free; do **not** re-implement them:

- Standard CLI flags: `--output`, `--append`, `--tag`, `--verbose`,
  `--suppress-messages`, `--autotagfile`, `--number-entries`,
  `--columns-header`, `--custom-header`, `--add-to-time-stamps`,
  `--inactive-time-stamps`, `--version`, plus `--config` when a config
  parser name is set.
- Logging setup (use `logging.info/debug/error`, not `print`).
- Writing the Org file header and footer.
- Append mode (`-a`): the writer hashes entries by `:ID:` and skips
  duplicates already present in the output file.
- Config file handling: pass `use_config_parser_name="memacs-<name>"`
  to the constructor (in the `bin/` script), then read options with
  `self._get_config_option("foo")`. Config files live under
  `$XDG_CONFIG_HOME/memacs/` and are matched by name.
- Error handling: exceptions from `_main()` are caught in
  `handle_main()` and logged into an `error.org` agenda entry when an
  output file is set.

### Reuse from `memacs.lib.orgwriter.OrgOutputWriter`

`self._writer.write_org_subitem(timestamp, output, note="", properties=OrgProperties(), tags=None)`
is the *only* call you should normally need to emit an entry. It
handles indentation, drawer layout, tags, append-mode deduping,
timestamp deltas (`--add-to-time-stamps`), and active/inactive
timestamps (`--inactive-time-stamps`). Do not concatenate Org-mode
markup by hand.

- `timestamp` must be a string produced by `OrgFormat.date(...)` (from
  the external `orgformat` package), or `False`/`None` for no
  timestamp. `OrgFormat.date` takes a `time.struct_time`.
- `tags` is a list of plain strings.

### Reuse from `memacs.lib.orgproperty.OrgProperties`

Build the `:PROPERTIES:` drawer with this class. The `:ID:` is hashed
automatically — never set it manually unless you truly have a stable
external unique id (then use `properties.set_id(...)`).

Two construction patterns:

1. No interesting properties — pass `data_for_hashing="<unique seed>"`
   to the constructor so the ID hash is unique.
2. Properties carry the uniqueness — call `properties.add("KEY", "value")`
   for each one; optionally also pass `data_for_hashing=...` to
   disambiguate when properties alone aren't unique.

### Reuse from `memacs.lib.reader`

`CommonReader.get_data_from_file(path)` and
`CommonReader.get_data_from_url(url)` for input I/O. `UnicodeDictReader`
for CSV-style input.

### Use the right tool for the input shape

- **HTML** → use `pypandoc.convert_text(html, "org", format="html",
  extra_args=["--wrap=none"])`. Pandoc handles links, bold, lists,
  entities, comments faithfully — far better than ad-hoc regex. Only
  pre-process HTML when you need to *strip* something pandoc would
  faithfully render but shouldn't (e.g. `memacs/podcastaddict.py`
  strips in-app `podcastaddict:N` anchors so they don't become useless
  `[[podcastaddict:0][…]]` Org links).
- **SQLite from a compressed backup** → extract into
  `tempfile.TemporaryDirectory()` and open read-only via the URI form:
  `sqlite3.connect("file:%s?mode=ro" % path, uri=True)`. Never write
  back to the extracted copy.
- **CSV** → `UnicodeDictReader` from `memacs.lib.reader`.
- **An external CLI tool** → `subprocess.check_output(...)`, but
  guard the call site with `shutil.which("<binary>")` and only do the
  check when the code path actually needs the binary (see
  `memacs/arbtt.py` for the pattern: skip the check when the user
  supplied an alternative input).

### What stays in the `bin/` script

Only metadata and the `main()` wrapper. Copy the pattern verbatim from
`bin/memacs_example.py` and adjust:

- `PROG_VERSION_NUMBER`, `PROG_VERSION_DATE`
- `PROG_SHORT_DESCRIPTION` (appears in the top-level Org headline)
- `PROG_TAG` (default `:Memacs:<tag>:` on the top entry)
- `PROG_DESCRIPTION` (shown in `--help`; include a sample config
  snippet here if the module reads a config file)
- `COPYRIGHT_YEAR`, `COPYRIGHT_AUTHORS`
- Uncomment `CONFIG_PARSER_NAME = "memacs-<name>"` and the
  `use_config_parser_name=` constructor argument only if a config file
  is needed.

Don't add CLI parsing or business logic to the `bin/` script.

## Writing a new module — checklist

1. **Module**: add `memacs/<name>.py` defining a subclass of `Memacs`
   that overrides only the three hooks above (`_parser_add_arguments`,
   `_parser_parse_args`, `_main`).
2. **Entry point**: add `bin/memacs_<name>.py` from the template
   (`bin/memacs_example.py`). Keep it free of logic.
3. **`pyproject.toml`** (two places):
   - Under `[project.scripts]`, add
     `memacs_<name> = "bin.memacs_<name>:main"` (alphabetical).
   - If the module needs extra Python packages, add them under
     `[dependency-groups]` with the module's name as key, e.g.
     `podcastaddict = ["pypandoc"]`. Pick the same key as the
     module's `PROG_TAG` when possible so users can predict it.
4. **External binaries**: if the module shells out to a non-Python
   tool (e.g. `pandoc`, `arbtt-stats`), call it out in the module's
   docs (next step) so users know what to install. Don't try to
   install it from `pyproject.toml`.
5. **Docs**: add `docs/memacs_<name>.org`. Mirror the structure of the
   other doc files (`docs/memacs_rss.org`, `docs/memacs_podcastaddict.org`):
   *Data Source*, *Options*, *Dependencies* (if non-trivial),
   *Automatic appending* (if applicable), *Output format*, *Example
   Invocation*, *Example Orgmode entry*.
6. **README + INSTALL touchpoints**:
   - Add the module to the alphabetical list in `README.org` under
     "Memacs Modules".
   - Add an entry under the current version in `README.org`'s
     Changelog ("Features" subsection).
   - If you added a new dependency group, add it to the groups list
     in both `README.org` (Installation) and `INSTALL.org` (and
     mention any required external binary in `INSTALL.org`).
7. **Unit test**: add `memacs/tests/<name>_test.py` modeled on
   `example_test.py`: construct the module with `argv=...` (always
   include `-s` to suppress log output), call `test_get_entries()`,
   and assert line-by-line on the returned list. Drop test fixtures
   under `memacs/tests/data/`. For data sources whose realistic
   fixtures would be large (DB backups, mailboxes, archive ZIPs),
   hand-craft a minimal synthetic fixture rather than checking in
   the real thing.
8. **Run the suite** (next section) and make sure it passes before
   considering the module done. Also do a smoke run against real data
   if you have any: `uv run memacs_<name> --help`, then
   `uv run memacs_<name> -s -o /tmp/out.org <real args>`.

## Working from real data

When a user describes a data source's schema, treat it as a hint and
**verify against an actual sample** before relying on it. Real
schemas routinely differ from what people remember:

- column names may differ in case (`seasonNB` documented, `seasonNb`
  in the database)
- "missing value" sentinels (`-1`, `0`, empty string) coexist with
  proper `NULL`s — filter for both
- the field that flags a row as "done" / "finished" / "read" is often
  not the one you'd guess; check distributions
  (`SELECT col, COUNT(*) FROM t GROUP BY col`)

If a sample data file is in the working tree (e.g. under
`temporary_dir_*/`), probe it directly with a throwaway script before
writing module SQL or parsers.

## Tests

Run the full suite:

```
./run_all_unit_tests.sh
```

This is a thin wrapper around
`uv run --group dev pytest --exitfirst memacs/tests memacs/lib/tests`.
Extra pytest args pass through.

Single module:

```
uv run --group dev pytest memacs/tests/<name>_test.py -v
```

When asserting against output, remember that `test_get_entries()`
strips the file header and footer and returns the body as a list of
lines (whitespace-significant — `\t` precedes inline tag groups).

## House rules

- Python 3.9+.
- Use `logging` (not `print`). `logging.error(...)` followed by
  `sys.exit(1)` is the standard fatal-error pattern.
- Don't hand-write Org-mode markup; go through `OrgOutputWriter` and
  `OrgProperties`.
- Don't bypass `handle_main()` — it provides the exception → error.org
  bridge that makes failures visible in the agenda.
- Keep the `bin/` script free of logic; if you find yourself adding
  argparse calls there, move them into the module's
  `_parser_add_arguments`.
- All timestamps go through `OrgFormat.date(time.localtime(seconds),
  show_time=True)`. For sources that store epoch milliseconds, divide
  by 1000. Use local time unless the source clearly stores something
  else — `time.localtime()` matches the typical "when did this
  happen on my device" interpretation users expect.
- Preserve the existing module style when patching contributor code,
  even if it diverges from the example — but new code should follow
  the example template.
