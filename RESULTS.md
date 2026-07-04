# c-stdlib-file-io-footgun-lab RESULTS

**Claim precision:** pass/fail/skip counts below are **compiler-backed C execution results**.

compiler_selected: zig cc
compiler_path: /tmp/zig-x86_64-linux-0.14.1/zig
compiler_version: zig 0.14.1
compile_command: /tmp/zig-x86_64-linux-0.14.1/zig cc -std=c11 -Wall -Wextra -O2 -o ./c_harness c_file_io_footgun_harness.c
compile_ok: True
compile_elapsed: 0.2295s
harness_elapsed: 0.0095s

**C harness status: compiled and executed.**

case_count: 50
method_count: 17
pass_count: 446
fail_count: 6
skip_count: 398
naive_expected_fail_count: 6

## counts by method
- preserve_original_case_baseline: 50
- compiler_discovery_checker: 50
- c_harness_compile_checker: 50
- fopen_fclose_policy_observer: 50
- fread_policy_observer: 50
- fgets_policy_observer: 50
- fgetc_eof_policy_observer: 50
- feof_ferror_clearerr_marker: 50
- seek_tell_marker: 50
- text_binary_scope_marker: 50
- path_encoding_scope_marker: 50
- wrapper_policy_marker: 50
- parser_design_scope_marker: 50
- safety_scope_marker: 50
- copy_size_timing_marker: 50
- naive_file_io_marker: 44
- external_platform_truth_not_tested_marker: 50

## artifacts
- cases.json: 22383 bytes
- fixtures/: 253 bytes total
- c_file_io_footgun_harness.c: 3375 bytes
- compiled binary: 17376 bytes
- results_rows.csv / results_rows.json

## environment
- python: 3.12.3
- platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- timing: time.perf_counter
- total_elapsed: 0.4323s

## scope / honesty
- HN-thread-access: yes, via Hacker News API CLI, thread id 32467610
  - committed evidence: `hn_thread_evidence.md`, `hn_comments_sanitized.txt`, `hn_nodes_sanitized.json`
- network/API/package-manager during benchmark: none, except HN fetch beforehand
- undefined-behavior-not-run: yes – invalid FILE*, use-after-fclose, OOB reads/writes, attacker paths – all not run
- file-io-scope: toy local lab, Python policy observers + C harness execution
- portability-not-tested: z/OS, EBCDIC, Windows wide paths, POSIX read/open – marked not_tested
- production-parser-not-tested: CSV/config/log parsing, Unicode decoding, locale databases – marked not_tested
- no z/OS, no IBM runtime, no Windows APIs, no fuzzing, no sanitizers, no static analyzers

## conclusions

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
- naive methods (feof-before-read, fread returns bytes, fgets always whole line, strlen for binary length, EOF==error, text==binary everywhere, paths always UTF-8) fail expected cases.
- this toy lab does NOT prove production input safety, z/OS behavior, POSIX behavior, Windows path behavior, locale/encoding behavior, etc.
