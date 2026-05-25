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
4. **Unit tests** (`memacs/tests/` and `memacs/lib/tests/`).

Many modules were contributed by peers, so style varies. The canonical
shape of a module is defined by the three example files referenced below.

## Required reading before adding or changing a module

Always study these together — they document the intended pattern:

- `bin/memacs_example.py` — entry-point template.
- `memacs/example.py` — module template (`Foo` subclass of `Memacs`).
- `memacs/tests/example_test.py` — test template using `test_get_entries()`.

When in doubt, compare against an existing module that already handles a
similar input (e.g. `memacs/csv.py` + `bin/memacs_csv.py` for tabular
input, `memacs/rss.py` for feed-style input).

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

1. Add `memacs/<name>.py` defining a subclass of `Memacs` that
   overrides only the three hooks above.
2. Add `bin/memacs_<name>.py` from the template.
3. Add a console-script entry to `setup.py` under
   `entry_points.console_scripts`. If the module needs extra Python
   dependencies, register them under `extras_require` and tag the
   entry with `[<extra>]` (e.g. `[gps]`).
4. Add a unit test `memacs/tests/<name>_test.py` modeled on
   `example_test.py`: construct the module with `argv=...` (always
   include `-s` to suppress log output), call `test_get_entries()`,
   and assert line-by-line on the returned list. Drop test fixtures
   under `memacs/tests/data/`.
5. Run the suite (see below) and make sure it passes before considering
   the module done.

## Tests

Run from the repo root:

```
PYTHONPATH=. pytest memacs/tests memacs/lib/tests
```

(The shell helper `run_all_unit_tests.sh` activates the local
`venv/` and runs `pytest --exitfirst` from inside `memacs/`.)

For a single module: `pytest memacs/tests/<name>_test.py -v`.

When asserting against output, remember that `test_get_entries()`
strips the file header and footer and returns the body as a list of
lines (whitespace-significant — `\t` precedes inline tag groups).

## House rules

- Python 3 only.
- Use `logging` (not `print`). `logging.error(...)` followed by
  `sys.exit(1)` is the standard fatal-error pattern.
- Don't hand-write Org-mode markup; go through `OrgOutputWriter` and
  `OrgProperties`.
- Don't bypass `handle_main()` — it provides the exception → error.org
  bridge that makes failures visible in the agenda.
- Keep the `bin/` script free of logic; if you find yourself adding
  argparse calls there, move them into the module's
  `_parser_add_arguments`.
- Preserve the existing module style when patching contributor code,
  even if it diverges from the example — but new code should follow
  the example template.
