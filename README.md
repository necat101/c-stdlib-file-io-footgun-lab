# c-stdlib-file-io-footgun-lab

Toy local correctness lab about C stdio file reading, driven by a real Hacker News thread.

HN thread: https://news.ycombinator.com/item?id=32467610 — "There are many ways to fail to read a file in a C program"

## Hacker News thread access

The Hacker News thread was read using the Hacker News API CLI (`hackernews` skill, Firebase API) **before writing this README**. ~75 comments were fetched (thread id 32467610).

Committed evidence artifacts:
- `hn_thread_evidence.md` – auditable summary with comment IDs and sentiment themes
- `hn_comments_sanitized.txt` – full comment text dump (~75 comments)
- `hn_nodes_sanitized.json` – raw HN API node data

This README reflects actual HN discussion themes, not just the linked blog post. Do NOT treat the linked article or cppreference docs alone as sufficient – the HN thread is the primary sentiment source.

## What HN users were actually debating

Summary of sentiments from the HN thread (paraphrased):

- **The linked article is largely about z/OS / IBM mainframe behavior, not universal ISO C.** Multiple commenters argued the article's file-reading pitfalls are specific to IBM's record-oriented datasets, EBCDIC, and vendor-specific fopen mode extensions – "the streams discussed in the article are neither text nor binary. They're record-oriented files, which are not supported by the C language standard." Others countered that C programmers still inherit the standard-library interface and must handle the practical mess.
- **"Standard C file I/O" versus POSIX read/open versus vendor-specific runtime behavior came up repeatedly.** Commenters debated whether the problems were C's fault, the C standard library's fault, or the target platform's fault (z/OS, Windows, Unix).
- **FILE*, fread, fgets, fscanf, fopen came up as the "standard" C file-reading interface.** The debate was about whether this interface is adequate for portable file reading.
- **fread's size/nmemb return semantics matter.** Returns completed items, not bytes, unless size is 1. Easy footgun.
- **fgets newline retention and truncation matter.** fgets retains newline if present, truncates long lines, returns NULL on EOF. Buffer size handling is error-prone.
- **feof/ferror after a read came up.** EOF is discovered by attempting a read, NOT by pre-checking feof. feof-before-read loops are a classic footgun. EOF and ferror are separate states.
- **EOF as an int sentinel matters.** fgetc returns int so EOF (-1) can be distinguished from all 256 unsigned char byte values (including 0xFF).
- **Text versus binary streams and implementation-defined transformations came up.** CRLF translation, EBCDIC conversion, record-oriented files – all platform-specific. Text mode behavior is implementation-defined.
- **Record-oriented files and vendor extensions came up heavily.** z/OS datasets, fixed-length records, IBM fopen mode strings with "keyword arguments" – not ISO C, but real-world C programmers on those platforms must deal with them.
- **File paths as byte strings versus text strings came up extensively.** Unix: paths are 0x00-terminated, 0x2F-separated byte sequences – NOT necessarily UTF-8. Windows: paths are 16-bit wide character sequences (UTF-16/WTF-16), _wfopen, etc. Rust PathBuf/OsString, Python surrogate escapes, all came up. "File names are 'stringy' in nature – people expect to be able to display them – and that means you need to have some up-front agreement on how to interpret those strings."
- **UTF-8, non-UTF-8 Unix names, Windows wide paths, Rust PathBuf/OsString, Python surrogate escapes, z/OS, and EBCDIC all came up.** Path encoding is a major cross-platform footgun separate from file content encoding.
- **Wrappers and project-local file-read policies came up.** "Basically every C/C++ project has a wrapper to fix [path encoding]". Reading files correctly requires project-level policy decisions.
- **"Read a file" is different from "correctly parse a portable document format".** The C stdio layer is just the first step – real parsing (CSV, config, logs, Unicode) is a whole separate problem.
- **C versus the C standard library versus the platform.** Commenters argued about whether blame belongs to C the language, the stdlib, or IBM/Microsoft/Unix platform quirks. "C has nothing to do with this. You'll have the same problems reading from Java." vs "C aged really well for a 1970s language supporting a zoo of computers."
- **Rust/Python path models came up as comparisons.** Rust's OsString/PathBuf distinguishing between text strings and OS paths, Python's surrogate escapes for undecodable filenames.
- **POSIX read/open versus ISO C fopen came up.** Some commenters preferred POSIX byte-oriented read() over stdio buffering complexity.

The thread also touched on: Microsoft _wfopen wide-char path functions, Go's os package passing 0666 permissions on Windows (ignored), content-addressable storage vs hierarchical filesystems, K&R C book and Unicode anachronism, whether UTF-8 handling belongs in the language or the programmer's responsibility, and whether filesystems themselves are an outdated concept.

## Lab scope

This is a **toy local correctness lab, NOT** a production file reader, libc conformance suite, z/OS emulator, Windows path lab, CSV/config/log parser, network protocol parser, filesystem portability suite, fuzzing target, sanitizer lab, or static analyzer.

- Deterministic synthetic fixture files only, generated by the repo itself. Fake labels like fake_file, demo_stream, synthetic_record, toy_line, etc.
- No real files, credentials, command-line arguments, protocol inputs, downloaded corpora, real system config files, real logs, or external parsers.
- No apt/sudo/root, no Docker, no external C libraries, no z/OS access, no IBM runtime, no Windows-only APIs, no build systems, no fuzzers, no sanitizers, no static analyzers.
- Python stdlib only for orchestration.
- **C harness validated with zig cc 0.14.1** – see `RESULTS.md` / `VERIFY.md`.
- UB cases (invalid FILE*, use-after-fclose, OOB reads/writes, attacker-controlled paths) are **marked skip / not_run, never executed**.

The point: test the HN debate in a tiny reproducible way – fread size/nmemb semantics, fgets newline retention/truncation, feof-after-read policy, fgetc int return, text/binary mode portability caveats, path encoding policy, and wrapper API design. Distinguish carefully between HN commenter opinions, ISO C guarantees, POSIX/vendor APIs, and local libc observations.

## Running

```bash
python3 -m py_compile generate_cases.py run_lab.py
python3 generate_cases.py   # writes cases.json + fixtures/, 50 cases
python3 run_lab.py          # compiler discovery → harness compile → run → RESULTS.md
```

`run_lab.py` discovers compilers in order: zig cc, cc, clang, gcc.

**Validated with zig cc 0.14.1** – see `VERIFY.md` for full transcript.

## Repository layout

- `generate_cases.py` – deterministic fake file I/O cases + fixture file generation (50 cases)
- `run_lab.py` – compiler discovery, harness compile/run, policy observers, writes RESULTS.md + results_rows.csv/json
- `c_file_io_footgun_harness.c` – C harness demonstrating fopen/fclose/fread/fgets/fgetc/feof/ferror/clearerr/rewind/fseek/ftell + project-local `read_result_t` wrapper. **Validated with zig cc 0.14.1.**
- `fixtures/` – generated synthetic fixture files
- `cases.json` – generated
- `RESULTS.md` – summary tables, skip matrix, compiler status, conclusions
- `results_rows.csv` / `results_rows.json` – per-case/per-method artifact
- `hn_thread_evidence.md` – HN thread evidence summary with comment IDs
- `hn_comments_sanitized.txt` – full HN comment text dump
- `hn_nodes_sanitized.json` – raw HN API node data
- `VERIFY.md` – fresh-clone verification transcript with **zig cc 0.14.1 compiler-backed C harness validation**

## Case coverage (50 cases)

fopen missing-file, text-file success, binary-file success, fclose status; fread byte reads, item-count pitfall, short-read, partial final item, zero-size, embedded NUL, no NUL-termination, manual NUL after read; fgets newline retained, final line without newline, long-line truncation, buffer-size-one, empty file, embedded NUL, strlen-after-fgets caveat; fgetc valid int, EOF after last byte, 0xFF not EOF; feof before read (footgun), feof after last byte, feof after failed read, ferror normal, clearerr resets EOF, rewind resets EOF; fseek/ftell offset, ftell text-mode portability caveat; text-mode newline portability, binary-mode byte preservation, CRLF translation caveat; z/OS not tested, EBCDIC not tested, Windows wide paths not tested, POSIX read not main impl, fscanf not used as file reader, path bytes vs text policy, locale encoding not tested; wrapper bytes_read, eof/error separate, reject partial record, accept streaming chunk; naive feof loop, naive fread nmemb, naive strlen binary; external platform truth not tested, production parser not tested, safety caveat.

## Methods compared

preserve_original_case_baseline, compiler_discovery_checker, c_harness_compile_checker, fopen_fclose_policy_observer, fread_policy_observer, fgets_policy_observer, fgetc_eof_policy_observer, feof_ferror_clearerr_marker, seek_tell_marker, text_binary_scope_marker, path_encoding_scope_marker, wrapper_policy_marker, parser_design_scope_marker, safety_scope_marker, copy_size_timing_marker, naive_file_io_marker, external_platform_truth_not_tested_marker.

Naive method intentionally assumes feof should be checked before reading, assumes fread returns bytes regardless of size/nmemb, assumes fgets always returns whole logical lines, assumes fgets output can always be measured with strlen even for binary data, assumes EOF and error are the same, assumes text and binary mode behave the same everywhere, assumes paths are always UTF-8 – and fails expected cases.

## What this lab does NOT prove

- Does NOT prove production input safety
- Does NOT prove z/OS behavior locally
- Does NOT prove POSIX behavior universally
- Does NOT prove Windows path behavior
- Does NOT prove locale/encoding behavior across systems
- Does NOT prove libc conformance
- Does NOT prove any wrapper is production-ready
- Does NOT test real CSV/config/log parsing
- Does NOT test sanitizers, fuzzers, static analyzers

Safe claims distinguish: HN commenter sentiments vs linked article claims vs ISO C guarantees vs POSIX/vendor APIs vs local libc behavior vs toy lab observations.

---

License: public domain / CC0 – toy lab.
