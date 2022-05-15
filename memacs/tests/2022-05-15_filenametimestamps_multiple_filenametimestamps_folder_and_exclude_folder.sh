#!/bin/bash

# create temp dir for example data
TMPDATADIR=$(mktemp -d --suffix="test_filenametimestamps_tmpdata")

# create temp dir for output
TMPOUTPUTDIR=$(mktemp -d --suffix="test_filenametimestamps_output")

# create 3 subdirs in temp dir
mkdir "${TMPDATADIR}/a"
mkdir "${TMPDATADIR}/b"
mkdir "${TMPDATADIR}/c"

# create multiple files in subdirs of temp dir
touch "${TMPDATADIR}/a/1-foo"
touch "${TMPDATADIR}/a/2-foo"
touch "${TMPDATADIR}/a/3-foo"
mkdir "${TMPDATADIR}/a/dir1"
touch "${TMPDATADIR}/a/dir1/1-bar"
mkdir "${TMPDATADIR}/a/dir2"
touch "${TMPDATADIR}/a/dir2/1-bar"
mkdir "${TMPDATADIR}/a/dir3"
touch "${TMPDATADIR}/a/dir3/1-bar"

touch "${TMPDATADIR}/b/1-foo"
touch "${TMPDATADIR}/b/2-foo"
touch "${TMPDATADIR}/b/3-foo"

touch "${TMPDATADIR}/c/1-foo"
touch "${TMPDATADIR}/c/2-foo"
touch "${TMPDATADIR}/c/3-foo"

## RESULT:
##
## tmpdata/a/1-foo
## tmpdata/a/2-foo
## tmpdata/a/3-foo
## tmpdata/a/dir1/1-bar
## tmpdata/a/dir2/1-bar
## tmpdata/a/dir3/1-bar
## 
## tmpdata/b/1-foo
## tmpdata/b/2-foo
## tmpdata/b/3-foo
##
## tmpdata/c/1-foo
## tmpdata/c/2-foo
## tmpdata/c/3-foo

## routine to visualize fails:
handle_fail() {
        echo
        echo "Test FAILS:"
        echo
        echo "missing entries:"
        diff "${OUTPUTFILE}_GREP_SED_EXPECTED" "${OUTPUTFILE}_GREP_SED_FOUND" | egrep '^<'
        echo
        echo "unexpected entries:"
        diff "${OUTPUTFILE}_GREP_SED_EXPECTED" "${OUTPUTFILE}_GREP_SED_FOUND" | egrep '^>'
        echo
    }

echo "------------------------------------------------------------------------------"
echo "Test 1: run filenametimestamp module: one index, one exclude:"

OUTPUTFILEBASENAME="test1_index-abc-ignore-only-c.org"
OUTPUTFILE="${TMPOUTPUTDIR}/${OUTPUTFILEBASENAME}"
PYTHONPATH="${HOME}/src/memacs/" /home/vk/src/memacs/bin/memacs_filenametimestamps.py \
          -o "${OUTPUTFILE}" \
          -f "${TMPDATADIR}" \
          -x "${TMPDATADIR}/c" \
          --omit-drawers # --verbose

echo """tmpdata/a/1-foo
tmpdata/a/2-foo
tmpdata/a/3-foo
tmpdata/a/dir1/1-bar
tmpdata/a/dir2/1-bar
tmpdata/a/dir3/1-bar
tmpdata/b/1-foo
tmpdata/b/2-foo
tmpdata/b/3-foo""" > "${OUTPUTFILE}_GREP_SED_EXPECTED"

grep "file:" "${OUTPUTFILE}" | sed 's/.*_filenametimestamps_//' | sed 's/\]\[.*//' | \
    sort > "${OUTPUTFILE}_GREP_SED_FOUND"

success="true"
diff -q "${OUTPUTFILE}_GREP_SED_EXPECTED" "${OUTPUTFILE}_GREP_SED_FOUND" && echo "Test SUCCESS" || handle_fail

echo "------------------------------------------------------------------------------"
echo "Test 2: run filenametimestamp module: multiple index, multiple exclude:"

OUTPUTFILEBASENAME="test2_index-abc-ignore-a_dir1_dir2_c.org"
OUTPUTFILE="${TMPOUTPUTDIR}/${OUTPUTFILEBASENAME}"
PYTHONPATH="${HOME}/src/memacs/" /home/vk/src/memacs/bin/memacs_filenametimestamps.py \
          -o "${OUTPUTFILE}" \
          -f "${TMPDATADIR}/a"  -f "${TMPDATADIR}/b"  -f "${TMPDATADIR}/c" \
          -x "${TMPDATADIR}/a/dir1" -x "${TMPDATADIR}/a/dir2" -x "${TMPDATADIR}/c" \
          --omit-drawers # --verbose

echo """tmpdata/a/1-foo
tmpdata/a/2-foo
tmpdata/a/3-foo
tmpdata/a/dir3/1-bar
tmpdata/b/1-foo
tmpdata/b/2-foo
tmpdata/b/3-foo""" > "${OUTPUTFILE}_GREP_SED_EXPECTED"

grep "file:" "${OUTPUTFILE}" | sed 's/.*_filenametimestamps_//' | sed 's/\]\[.*//' | \
    sort > "${OUTPUTFILE}_GREP_SED_FOUND"

success="true"
diff -q "${OUTPUTFILE}_GREP_SED_EXPECTED" "${OUTPUTFILE}_GREP_SED_FOUND" && echo "Test SUCCESS" || handle_fail

# cleanup
#rm -rf "${TMPDATADIR}" "${TMPOUTPUTDIR}"

#end
