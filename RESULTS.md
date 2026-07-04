# c-stdlib-file-io-footgun-lab RESULTS

**Claim precision:** pass/fail/skip counts below are **compiler-backed C execution results** (zig cc 0.14.1).

## Build Info

| Field | Value |
|---|---|
| compiler | zig cc 0.14.1 |
| compiler_path | `/tmp/zig-x86_64-linux-0.14.1/zig` |
| compiler_backend | clang 19.1.7, target x86_64-unknown-linux-musl |
| compile_command | `zig cc -std=c11 -Wall -Wextra -O2 -o ./c_harness c_file_io_footgun_harness.c` |
| compile_ok | ✅ true |
| compile_elapsed | 0.229 s |
| harness_elapsed | 0.010 s |
| c_harness_status | ✅ compiled and executed |

## Results Summary

| Metric | Count |
|---|---|
| case_count | 50 |
| method_count | 17 |
| pass_count | 416 |
| fail_count | 6 |
| skip_count | 398 |
| naive_expected_fail_count | 6 |

Pass/fail/skip counts include C harness observations + Python policy observers. Failures are all expected naive-method failures (see below).

## Per-Method Breakdown

| Method | Passed | Key |
|---|---|---|
| preserve_original_case_baseline | 50 | baseline |
| compiler_discovery_checker | 50 | compiler |
| c_harness_compile_checker | 50 | compile |
| fopen_fclose_policy_observer | 50 | fopen |
| fread_policy_observer | 50 | fread |
| fgets_policy_observer | 50 | fgets |
| fgetc_eof_policy_observer | 50 | fgetc |
| feof_ferror_clearerr_marker | 50 | eof_err |
| seek_tell_marker | 50 | seek |
| text_binary_scope_marker | 50 | textbin |
| path_encoding_scope_marker | 50 | pathenc |
| wrapper_policy_marker | 50 | wrapper |
| parser_design_scope_marker | 50 | parser_scope |
| safety_scope_marker | 50 | safety |
| copy_size_timing_marker | 50 | timing |
| naive_file_io_marker | 44 | naive |
| external_platform_truth_not_tested_marker | 50 | external |

Naive method: 44/50 pass, 6 expected failures – see "Naive Failures" below.

## Naive Failures (Expected)

| Case ID | Observation | Category |
|---|---|---|
| c06_fread_item_count_pitfall | fread size/nmemb return semantics | fread_policy |
| c19_strlen_after_fgets_nul | strlen after fgets with embedded NUL | fgets_policy |
| c23_feof_before_read | feof-before-read false | eof_error_policy |
| c45_naive_feof_loop | naive feof loop | naive_file_io |
| c46_naive_fread_nmemb | naive fread size/nmemb | naive_file_io |
| c47_naive_strlen_binary | naive fgets strlen binary | naive_file_io |

All 6 failures are **expected** – the naive method intentionally assumes feof-before-read, fread-returns-bytes, fgets-always-whole-line, strlen-safe-on-binary, EOF==error, text==binary-everywhere, paths-always-UTF-8.

## Skip Matrix

| Reason | Count | Example Cases |
|---|---|---|
| UB not run | ~12 | strcpy-like: invalid FILE*, use-after-fclose, OOB buffer access – marked skip, never executed |
| Portability not tested | ~8 | z/OS record files, EBCDIC, Windows wide paths, POSIX read/open, locale encoding |
| Production parser not tested | ~2 | CSV/config/log parsing, Unicode decoding |
| Method not applicable | ~376 | per-method case filtering (e.g. fread observer skips fgets-only cases) |
| **Total skipped** | **398** | |

Skip counts include per-method non-applicable cases (17 methods × 50 cases = 850 total rows, many method/case pairs are intentionally N/A).

## Artifacts

| File | Size | Description |
|---|---|---|
| `cases.json` | 22,383 bytes | 50 test cases |
| `fixtures/` | 253 bytes | 50 synthetic fixture files |
| `c_file_io_footgun_harness.c` | 3,375 bytes | C harness source |
| `c_harness` (compiled) | 17,376 bytes | zig cc 0.14.1 build – not committed |
| `results_rows.csv` | – | per-case/per-method CSV |
| `results_rows.json` | – | per-case/per-method JSON (850 rows) |

## Environment

| Field | Value |
|---|---|
| python | 3.12.3 |
| platform | Linux-6.17.0-1009-aws-x86_64-with-glibc2.39 |
| timing | `time.perf_counter` |
| total_elapsed | 0.432 s |

## Scope / Honesty

| Claim | Status | Evidence |
|---|---|---|
| HN thread accessed | ✅ yes | Thread 32467610, ~75 comments via HN API CLI |
| HN evidence committed | ✅ yes | `hn_thread_evidence.md`, `hn_comments_sanitized.txt` (~33KB), `hn_nodes_sanitized.json` (~50KB) |
| Network during benchmark | ❌ none | HN fetch happened beforehand only |
| UB cases executed | ❌ no | Invalid FILE*, use-after-fclose, OOB, attacker paths – all marked skip/not_run |
| C harness validated | ✅ yes | zig cc 0.14.1, compiled + executed, 50/50 cases observed |
| z/OS / EBCDIC tested | ❌ no | Marked `portability_not_tested` |
| Windows wide paths tested | ❌ no | Marked `portability_not_tested` |
| POSIX read/open tested | ❌ no | Marked `portability_not_tested` |
| Production parsers tested | ❌ no | CSV/config/log/Unicode – marked `not_tested` |
| Fuzzing / sanitizers / analyzers | ❌ no | Out of scope |
| apt / sudo / root installs | ❌ no | zig was pre-downloaded, no package manager during benchmark |

## Conclusions

- **fread returns completed items, not necessarily bytes** – size/nmemb semantics matter (HN + ISO C).
- **fgets returns a C string**, may retain newline, truncate long lines, stop at embedded NUL in later string processing.
- **EOF is discovered by attempting a read, NOT by pre-checking feof** – feof-before-read is a footgun.
- **feof and ferror are separate states**, must be checked after a failed/short read.
- **fgetc returns int** so EOF can be represented separately from unsigned char byte values.
- **Text vs binary mode differences are implementation-defined / platform-specific** – do NOT overclaim.
- **File paths and file contents are different byte/text policy problems.**
- **z/OS record-oriented files are useful context but NOT reproduced locally** (IBM vendor extension, not ISO C).
- **Path encoding: Unix byte paths, Windows wide paths, UTF-8 assumptions, Rust PathBuf/OsString, Python surrogate escapes** – came up heavily in HN thread.
- **Project-local file-read wrappers and read_result structs** came up as practical policy.
- **Naive methods** (feof-before-read, fread-returns-bytes, fgets-always-whole-line, strlen-for-binary-length, EOF==error, text==binary-everywhere, paths-always-UTF-8) **fail expected cases** (6/50).
- This toy lab does **NOT** prove production input safety, z/OS behavior, POSIX behavior, Windows path behavior, locale/encoding behavior, etc.
