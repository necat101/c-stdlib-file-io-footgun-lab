# c-stdlib-file-io-footgun-lab RESULTS

**Claim precision:** pass/fail/skip counts below are **compiler-backed C execution results**.

## Build Info

| Field | Value |
|---|---|
| compiler | zig cc |
| compiler_path | `/tmp/zig-x86_64-linux-0.14.1/zig` |
| compiler_version | zig 0.14.1 |
| compile_command | `/tmp/zig-x86_64-linux-0.14.1/zig cc -std=c11 -Wall -Wextra -O2 -o ./c_harness c_file_io_footgun_harness.c` |
| compile_ok | ✅ true |
| compile_elapsed | 0.2759s |
| harness_elapsed | 0.0146s |
| c_harness_status | compiled and executed |

## Results Summary

| Metric | Count |
|---|---|
| case_count | 50 |
| method_count | 17 |
| pass_count | 446 |
| fail_count | 6 |
| skip_count | 398 |
| naive_expected_fail_count | 6 |

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

## Naive Failures (Expected)

| Case ID | Observation | Category |
|---|---|---|
| c06_fread_item_count_pitfall | fread item-size-count pitfall | fread_policy |
| c19_strlen_after_fgets_nul | strlen-after-fgets-embedded-NUL caveat | fgets_policy |
| c23_feof_before_read | feof-before-read false | eof_error_policy |
| c45_naive_feof_loop | naive-feof-loop | naive_file_io |
| c46_naive_fread_nmemb | naive-fread-size-nmemb | naive_file_io |
| c47_naive_strlen_binary | naive-fgets-strlen-binary | naive_file_io |

## Skip Matrix

| Reason | Count |
|---|---|
| Total skipped | 398 |
| UB not run | ~ | invalid FILE*, use-after-fclose, OOB – marked skip |
| Portability not tested | ~ | z/OS, EBCDIC, Windows wide paths, POSIX read/open, locale |
| Production parser not tested | ~ | CSV/config/log parsing, Unicode decoding |
| Method not applicable | ~ | per-method case filtering |

## Artifacts

| File | Size | Description |
|---|---|---|
| `cases.json` | 22383 bytes | 50 test cases |
| `fixtures/` | 253 bytes | synthetic fixture files |
| `c_file_io_footgun_harness.c` | 3375 bytes | C harness source |
| `c_harness` (compiled) | 17376 bytes | zig cc build |
| `results_rows.csv` | – | per-case/per-method CSV |
| `results_rows.json` | – | per-case/per-method JSON |

## Environment

| Field | Value |
|---|---|
| python | 3.12.3 |
| platform | Linux-6.17.0-1009-aws-x86_64-with-glibc2.39 |
| timing | time.perf_counter |
| total_elapsed | 0.4873s |

## Scope / Honesty

| Claim | Status | Evidence |
|---|---|---|
| HN thread accessed | ✅ yes | Thread 32467610 via HN API CLI |
| HN evidence committed | ✅ yes | `hn_thread_evidence.md`, `hn_comments_sanitized.txt`, `hn_nodes_sanitized.json` |
| Network during benchmark | ❌ none | HN fetch beforehand only |
| UB cases executed | ❌ no | all marked skip/not_run |
| C harness validated | ✅ yes | zig cc 0.14.1 |
| z/OS / EBCDIC tested | ❌ no | marked `portability_not_tested` |
| Windows wide paths tested | ❌ no | marked `portability_not_tested` |
| Production parsers tested | ❌ no | marked `not_tested` |
| Fuzzing / sanitizers | ❌ no | out of scope |

## Conclusions

- fread returns completed items, not necessarily bytes – size/nmemb semantics matter (HN + ISO C).
- fgets returns a C string, may retain newline, truncate long lines, stop at embedded NUL in later string processing.
- EOF is discovered by attempting a read, NOT by pre-checking feof – feof-before-read is a footgun.
- feof and ferror are separate states, must be checked after a failed/short read.
- fgetc returns int so EOF can be represented separately from unsigned char byte values.
- text vs binary mode differences are implementation-defined / platform-specific – do NOT overclaim.
- file paths and file contents are different byte/text policy problems.
- z/OS record-oriented files are useful context but NOT reproduced locally (IBM vendor extension, not ISO C).
- path encoding: Unix byte paths, Windows wide paths, UTF-8 assumptions, Rust PathBuf/OsString, Python surrogate escapes – came up heavily in HN thread.
- project-local file-read wrappers and read_result structs came up as practical policy.
- naive methods (feof-before-read, fread-returns-bytes, fgets-always-whole-line, strlen-for-binary-length, EOF==error, text==binary-everywhere, paths-always-UTF-8) fail expected cases.
- this toy lab does NOT prove production input safety, z/OS behavior, POSIX behavior, Windows path behavior, locale/encoding behavior, etc.
