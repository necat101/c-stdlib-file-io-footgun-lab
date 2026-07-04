# VERIFY.md – fresh clone verification

Fresh-clone tested: **✅ YES – with compiler-backed C harness validation (zig cc 0.14.1).**

## Environment

| Field | Value |
|---|---|
| python | 3.12.3 |
| platform | Linux-6.17.0-1009-aws-x86_64-with-glibc2.39 |
| compiler | **zig cc 0.14.1** |
| compiler_path | `/tmp/zig-x86_64-linux-0.14.1/zig` |
| compiler_backend | clang 19.1.7, target x86_64-unknown-linux-musl |
| date | 2026-07-04 |

## Verification Transcript

### 1. py_compile

```sh
$ python3 -m py_compile generate_cases.py run_lab.py
py_compile_exit=0
```

✅ Pass

### 2. Generate cases + fixtures

```sh
$ python3 generate_cases.py
Wrote 50 cases to cases.json, fixtures in fixtures/
```

✅ 50 cases, 50 fixture files generated

### 3. Run lab (compiler discovery → compile → run)

```sh
$ python3 run_lab.py
compiler: zig cc /tmp/zig-x86_64-linux-0.14.1/zig zig 0.14.1
loaded 50 cases
compile: /tmp/zig-x86_64-linux-0.14.1/zig cc -std=c11 -Wall -Wextra -O2 -o ./c_harness c_file_io_footgun_harness.c
compile_ok True elapsed 0.1074s
harness run elapsed 0.0060s
wrote RESULTS.md, results_rows.csv/json
{'pass_count': 446, 'fail_count': 6, 'skip_count': 398, 'naive_expected_fail_count': 6, 'case_count': 50, 'method_count': 17, 'compiler': 'zig cc', 'compile_ok': True}
```

| Step | Status | Details |
|---|---|---|
| Compiler discovery | ✅ | zig cc 0.14.1 found |
| Harness compile | ✅ | `zig cc -std=c11 -Wall -Wextra -O2`, 0.11s |
| Harness run | ✅ | 50/50 cases observed, 0.006s |
| Policy observers | ✅ | fopen/fread/fgets/fgetc/feof/ferror all completed |
| Output artifacts | ✅ | RESULTS.md, results_rows.csv/json |

### 4. Direct harness run

```sh
$ ./c_harness cases.json
{"harness":"c_file_io_footgun","observations":[
  {"case_id":"c01_fopen_missing","c_harness":"ok"},
  {"case_id":"c02_fopen_text_ok","c_harness":"ok"},
  ...
  {"case_id":"c50_safety_caveat","c_harness":"ok"}
]}
```

✅ All 50 cases observed by C harness

## Results Summary

| Metric | Count |
|---|---|
| case_count | 50 |
| method_count | 17 |
| total_rows | 850 |
| pass_count | 446 |
| fail_count | 6 |
| skip_count | 398 |
| naive_expected_fail_count | 6 |

Failures are all **expected naive-method failures**:

| Case ID | Reason |
|---|---|
| c06_fread_item_count_pitfall | fread size/nmemb semantics |
| c19_strlen_after_fgets_nul | strlen after fgets with embedded NUL |
| c23_feof_before_read | feof-before-read footgun |
| c45_naive_feof_loop | naive feof loop |
| c46_naive_fread_nmemb | naive fread size/nmemb |
| c47_naive_strlen_binary | naive fgets strlen binary |

## Artifacts Produced

| File | Status | Notes |
|---|---|---|
| `cases.json` | ✅ | 50 test cases |
| `fixtures/` | ✅ | 50 synthetic fixture files |
| `c_file_io_footgun_harness.c` | ✅ | 3,375 bytes – **compiled + executed with zig cc 0.14.1** |
| `c_harness` (binary) | ✅ | ~16KB – not committed, reproducible |
| `RESULTS.md` | ✅ | summary tables, skip matrix, conclusions |
| `results_rows.csv` | ✅ | per-case/per-method CSV (850 rows) |
| `results_rows.json` | ✅ | per-case/per-method JSON |
| `hn_thread_evidence.md` | ✅ | HN audit trail |
| `hn_comments_sanitized.txt` | ✅ | ~75 comments, ~33KB |
| `hn_nodes_sanitized.json` | ✅ | raw API nodes, ~50KB |

## Scope Checklist

| Check | Status |
|---|---|
| py_compile passes | ✅ |
| cases + fixtures generated | ✅ |
| C harness compiled (zig cc) | ✅ |
| C harness executed (50/50) | ✅ |
| Policy observers completed | ✅ |
| UB cases NOT run | ✅ – marked skip |
| No network during benchmark | ✅ |
| No real files / parser input | ✅ |
| HN evidence committed | ✅ |
| Per-case artifacts committed | ✅ |

## Compiler Details

C harness validated with **zig cc 0.14.1** (clang 19.1.7 backend, musl target):

```sh
zig cc -std=c11 -Wall -Wextra -O2 -o c_harness c_file_io_footgun_harness.c
./c_harness cases.json
```

All 50 cases observed. UB cases (invalid FILE*, use-after-fclose, OOB reads/writes, attacker-controlled paths) are marked skip/not_run in case data and never passed to C file I/O functions unsafely.

Compiler discovery order: zig cc → cc → clang → gcc. Zig was used per lab preference.

---

**Result: Fresh-clone tested ✅ YES – with compiler-backed C harness validation (zig cc 0.14.1, 50/50 cases observed).**
