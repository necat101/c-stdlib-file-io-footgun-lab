# HN thread evidence – c-stdlib-file-io-footgun-lab

Thread: "There are many ways to fail to read a file in a C program"
URL: https://news.ycombinator.com/item?id=32467610
Article: https://colinpaice.blog/2022/08/06/there-are-many-ways-to-fail-to-read-a-file-in-a-c-program/
Fetched: 2026-07-04 via Hacker News API CLI (Firebase)
Tool: `hackernews` skill – `python3 ./hackernews get-item --id 32467610`

- Descendants: ~75 comments
- Comments fetched: 75

Committed evidence artifacts (in repo root):
- `hn_thread_evidence.md` (this file) – auditable summary with comment IDs and sentiment themes
- `hn_comments_sanitized.txt` – full comment text dump (~75 comments, ~33KB)
- `hn_nodes_sanitized.json` – raw HN API node data (~50KB)

## Key comment IDs (for audit)

- 32468109 (bregma) – "The one single standard way to read a file in C. There are (potentially infinite) many non-standard ways using third-party vendored libraries or vendor-specific extensions to the standard C library. This article discusses a small subset of the latter, specific to a single vendor."
- 32467935 (nemetroid) – "This seems to be about the z/OS C API."
- 32468183 (planede) – IBM fopen mode strings with "keyword arguments"
- 32468165 (nuc1e0n) – z/OS best practice: binary mode + wrappers for fread/fgets to convert to utf-8/unix newlines? fixed length records?
- 32468536 (edflsafoiewq) – Microsoft _wfopen wide-char path problems, "ensure the path has no unicode characters"
- 32468787 (mananaysiempre) – path encoding deep dive: Unix byte paths vs Windows wide paths (UTF-16/WTF-16), Rust PathBuf/OsString, Python surrogate escapes
- 32468619 (zokier) – Unix filenames are not UTF-8, Rust OsString footgun
- 32468357 (rmind) – C aged well for 1970s language, ASCII vs EBCDIC is computer architecture issue not language issue, Unicode didn't exist
- Multiple thread branches – K&R C book and Unicode anachronism debate
- 32470344+ – Python os.listdir() UTF-8 vs bytes path handling, surrogate escapes
- Various – POSIX vs C stdio, Go os package 0666 permissions on Windows, content-addressable storage vs hierarchical filesystems

## Sentiment themes extracted (used in README)

1. Article is largely about z/OS / IBM runtime behavior, NOT universal ISO C
2. "Standard C file I/O" vs POSIX read/open vs vendor-specific runtime
3. FILE*, fread, fgets, fscanf, fopen as the "standard" C file-reading interface
4. fread size/nmemb return semantics matter
5. fgets newline retention and truncation matter
6. feof/ferror after a read – EOF discovered by attempting read, NOT pre-checking
7. EOF as int sentinel – fgetc returns int
8. Text vs binary streams, implementation-defined transformations
9. Record-oriented files, vendor extensions (z/OS datasets)
10. File paths as byte strings vs text strings
11. UTF-8, non-UTF-8 Unix names, Windows wide paths, Rust PathBuf/OsString, Python surrogate escapes, z/OS, EBCDIC
12. Wrappers and project-local file-read policies
13. "Read a file" ≠ "correctly parse a portable document format"
14. C vs C standard library vs platform – where does blame belong?
15. Rust/Python path models as comparisons
16. POSIX read/open vs ISO C fopen

Full comment dump committed in repo:
- `hn_comments_sanitized.txt` – 75 comments, ~33KB
- `hn_nodes_sanitized.json` – raw HN API nodes, ~50KB

This file exists to make the HN-thread-reading step auditable. The README sentiment summary is derived from the above API-fetched comments, not from web search or the linked article alone. All HN evidence artifacts are committed to the repository.
