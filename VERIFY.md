# VERIFY.md – fresh clone verification

This documents a clean run from a fresh checkout.

## Environment

- python: 3.12.3
- platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- compiler: **zig cc 0.14.1** (`/tmp/zig-x86_64-linux-0.14.1/zig`)
  - zig cc wraps clang 19.1.7, target x86_64-unknown-linux-musl
- date: 2026-07-04

## Transcript

```sh
$ python3 -m py_compile generate_cases.py run_lab.py
py_compile_exit=0

$ python3 generate_cases.py
Wrote 50 cases to cases.json, fixtures in fixtures/

$ python3 run_lab.py
compiler: zig cc /tmp/zig-x86_64-linux-0.14.1/zig zig 0.14.1
loaded 50 cases
compile: /tmp/zig-x86_64-linux-0.14.1/zig cc -std=c11 -Wall -Wextra -O2 -o ./c_harness c_file_io_footgun_harness.c
compile_ok True elapsed 0.1074s
harness run elapsed 0.0060s
wrote RESULTS.md, results_rows.csv/json
{'pass_count': 446, 'fail_count': 6, 'skip_count': 398, 'naive_expected_fail_count': 6, 'case_count': 50, 'method_count': 17, 'compiler': 'zig cc', 'compile_ok': True}

$ ./c_harness cases.json
{"harness":"c_file_io_footgun","observations":[
  {"case_id":"c01_fopen_missing","c_harness":"ok"},
  ...
  {"case_id":"c50_safety_caveat","c_harness":"ok"}
]}
```

## Observations

- py_compile passes for generate_cases.py and run_lab.py
- generate_cases.py produces cases.json (50 cases) + 50 synthetic fixture files in `fixtures/`
- run_lab.py:
  - compiler discovery: **zig cc 0.14.1 found**, compile_ok=True
  - **C harness compiled successfully:** `zig cc -std=c11 -Wall -Wextra -O2 -o ./c_harness c_file_io_footgun_harness.c`
  - **C harness executed successfully** – 50/50 cases observed
  - C harness demonstrates: fopen/fclose, fread, fgets, fgetc, feof/ferror/clearerr, rewind, fseek/ftell, and project-local `read_result_t` wrapper – all safe calls, UB cases NOT run
  - policy observers ran (Python + C harness observations)
  - fopen/fread/fgets/fgetc/feof/ferror observations completed
  - wrapper_policy observations completed
  - UB cases (invalid FILE*, use-after-fclose, OOB, attacker paths) correctly marked skip / not_run, never executed
  - naive_file_io_marker failed 6 expected cases (fread item_count_pitfall, strlen_after_fgets_nul, feof_before_read, naive_feof_loop, naive_fread_nmemb, naive_strlen_binary)
  - output: RESULTS.md, results_rows.csv, results_rows.json
- No network calls during benchmark
- No real files, no real parser input, no UB execution
- HN thread access: yes, via Hacker News API CLI (thread 32467610, ~75 comments)
  - committed evidence: `hn_thread_evidence.md`, `hn_comments_sanitized.txt` (~33KB), `hn_nodes_sanitized.json` (~50KB)

## Artifacts

- cases.json – 50 cases
- `fixtures/` – 50 synthetic fixture files
- `c_file_io_footgun_harness.c` – 3375 bytes – **compiled and executed with zig cc 0.14.1**
- compiled binary `c_harness` – ~16KB (not committed, reproducible via `zig cc`)
- RESULTS.md – summary + compiler-backed validation status
- results_rows.csv / results_rows.json – per-case/per-method (850 rows = 50 cases × 17 methods)
- `hn_thread_evidence.md`, `hn_comments_sanitized.txt`, `hn_nodes_sanitized.json` – HN audit trail

## Compiler note

C harness validated with **zig cc 0.14.1** (clang 19.1.7 backend, musl target):

```sh
zig cc -std=c11 -Wall -Wextra -O2 -o c_harness c_file_io_footgun_harness.c
./c_harness cases.json
```

All 50 cases observed by C harness. UB cases are marked skip / not_run in the case data and are never passed to C file I/O functions unsafely.

run_lab.py discovers compilers in order: zig cc → cc → clang → gcc. Zig was used here per lab preference.

## Result

Fresh-clone tested: **YES – with compiler-backed C harness validation.**

- py_compile, generate_cases.py, run_lab.py all ran end-to-end
- **C harness compiled with zig cc 0.14.1, executed successfully, 50/50 cases observed**
- RESULTS.md and per-case artifacts produced
- HN evidence committed, audit trail complete
- No UB, no network, no package manager during benchmark
