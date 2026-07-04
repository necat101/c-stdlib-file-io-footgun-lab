#!/usr/bin/env python3
"""generate deterministic C file I/O footgun cases"""
import json, pathlib, os
cases = []
def add(cid, category, fake_name, fixture_name, fixture_bytes, read_buf_cap=None,
        fread_size=None, fread_nmemb=None, fgets_buf=None,
        operation="", expected="success", expected_obs="", notes=""):
    cases.append({
        "id": cid,
        "category": category,
        "fake_name": fake_name,
        "fixture_name": fixture_name,
        "fixture_bytes": fixture_bytes,
        "fixture_len": len(fixture_bytes.encode('latin1') if isinstance(fixture_bytes, str) else fixture_bytes),
        "read_buffer_capacity": read_buf_cap,
        "fread_size": fread_size,
        "fread_nmemb": fread_nmemb,
        "fgets_buffer_size": fgets_buf,
        "operation": operation,
        "expected": expected,
        "expected_obs": expected_obs,
        "notes": notes
    })

def b(s): return s  # fixture content as str, may include \n \x00 etc

# fopen/fclose
add("c01_fopen_missing", "fopen_policy", "fake_file", "missing_fixture.dat", "", None, None, None, None, "fopen", "error", "fopen missing-file error", "")
add("c02_fopen_text_ok", "fopen_policy", "demo_stream", "text_ok.txt", "hello\nworld\n", None, None, None, None, "fopen", "success", "fopen generated-text-file success", "")
add("c03_fopen_binary_ok", "fopen_policy", "synthetic_record", "binary_ok.bin", "AB\x00CD\xff", None, None, None, None, "fopen", "success", "fopen generated-binary-file success", "")
add("c04_fclose_status", "fopen_policy", "toy_line", "close_test.txt", "x\n", None, None, None, None, "fclose", "success", "fclose status marker", "")

# fread
add("c05_fread_bytes_exact", "fread_policy", "example_blob", "fread_exact.bin", "ABCDEFGH", 32, 1, 8, None, "fread", "success", "fread byte-size reads exact bytes", "")
add("c06_fread_item_count_pitfall", "fread_policy", "sample_text", "fread_items.bin", "12345678", 32, 4, 2, None, "fread", "success", "fread item-size-count pitfall", "naive_fail")
add("c07_fread_short_read", "fread_policy", "fake_config_line", "fread_short.bin", "short", 32, 1, 100, None, "fread", "success", "fread short-read item-count", "")
add("c08_fread_partial_final", "fread_policy", "demo_bytes", "fread_partial.bin", "1234567", 32, 4, 2, None, "fread", "success", "fread partial-final-item", "")
add("c09_fread_zero_size", "fread_policy", "synthetic_newline_file", "fread_zero.bin", "data", 32, 0, 10, None, "fread", "success", "fread zero-size-not-useful", "")
add("c10_fread_embedded_nul", "fread_policy", "toy_binary_blob", "fread_nul.bin", "A\x00B\x00C", 32, 1, 5, None, "fread", "success", "fread binary-embedded-NUL", "")
add("c11_fread_no_nul_term", "fread_policy", "fictional_path_bytes", "fread_nonul.bin", "DATA", 32, 1, 4, None, "fread", "success", "fread does-not-NUL-terminate", "")
add("c12_fread_manual_nul", "fread_policy", "fake_log_line", "fread_manul.bin", "test", 32, 1, 4, None, "fread", "success", "fread manual-NUL-after-byte-read", "")

# fgets
add("c13_fgets_newline_retained", "fgets_policy", "sample_short_read", "fgets_nl.txt", "hello\n", 32, None, None, 32, "fgets", "success", "fgets short-line-retains-newline", "")
add("c14_fgets_no_final_nl", "fgets_policy", "demo_record_file", "fgets_nonl.txt", "lastline", 32, None, None, 32, "fgets", "success", "fgets final-line-without-newline", "")
add("c15_fgets_truncation", "fgets_policy", "synthetic_eof_case", "fgets_long.txt", "this_is_a_very_long_line_that_exceeds_buffer\n", 16, None, None, 16, "fgets", "success", "fgets long-line-truncation", "")
add("c16_fgets_bufsize_one", "fgets_policy", "fake_buffer_case", "fgets_one.txt", "abc\n", 8, None, None, 1, "fgets", "success", "fgets buffer-size-one", "")
add("c17_fgets_empty", "fgets_policy", "fake_file", "fgets_empty.txt", "", 32, None, None, 32, "fgets", "success", "fgets empty-file returns NULL", "")
add("c18_fgets_embedded_nul", "fgets_policy", "demo_stream", "fgets_nul.txt", "a\x00bc\n", 32, None, None, 32, "fgets", "success", "fgets embedded-NUL-in-file", "")
add("c19_strlen_after_fgets_nul", "fgets_policy", "synthetic_record", "strlen_nul.txt", "x\x00y\n", 32, None, None, 32, "fgets", "success", "strlen-after-fgets-embedded-NUL caveat", "naive_fail")

# fgetc / EOF
add("c20_fgetc_valid_int", "fgetc_policy", "toy_line", "fgetc_ok.bin", "ABC", None, None, None, None, "fgetc", "success", "fgetc valid-byte-as-int", "")
add("c21_fgetc_eof_after", "fgetc_policy", "example_blob", "fgetc_eof.bin", "Z", None, None, None, None, "fgetc", "success", "fgetc EOF-after-last-byte", "")
add("c22_fgetc_ff_not_eof", "fgetc_policy", "sample_text", "fgetc_ff.bin", "\xff\xfe", None, None, None, None, "fgetc", "success", "fgetc byte-0xff-not-EOF", "")

# feof / ferror
add("c23_feof_before_read", "eof_error_policy", "fake_config_line", "feof_pre.txt", "data\n", None, None, None, None, "feof", "success", "feof-before-read false", "naive_fail")
add("c24_feof_after_last_byte", "eof_error_policy", "demo_bytes", "feof_last.txt", "x", None, None, None, None, "feof", "success", "feof-after-successful-last-byte false", "")
add("c25_feof_after_failed", "eof_error_policy", "synthetic_newline_file", "feof_fail.txt", "y", None, None, None, None, "feof", "success", "feof-after-failed-read true", "")
add("c26_ferror_normal", "eof_error_policy", "toy_binary_blob", "ferror_ok.txt", "ok\n", None, None, None, None, "ferror", "success", "ferror-normal-read false", "")
add("c27_clearerr_resets", "eof_error_policy", "fictional_path_bytes", "clearerr.txt", "a", None, None, None, None, "clearerr", "success", "clearerr resets EOF", "")
add("c28_rewind_resets", "eof_error_policy", "fake_log_line", "rewind.txt", "b", None, None, None, None, "rewind", "success", "rewind resets EOF", "")

# fseek / ftell
add("c29_seek_tell_offset", "seek_tell_policy", "sample_short_read", "seek.bin", "0123456789", None, None, None, None, "fseek", "success", "fseek-ftell basic-offset", "")
add("c30_ftell_text_caveat", "seek_tell_policy", "demo_record_file", "ftell_text.txt", "line1\nline2\n", None, None, None, None, "ftell", "success", "ftell-text-mode-portability caveat", "portability")

# text / binary
add("c31_text_mode_nl", "text_binary_caveat", "synthetic_eof_case", "text_nl.txt", "a\nb\n", None, None, None, None, "policy", "success", "text-mode-newline-portability", "portability")
add("c32_binary_preserve", "text_binary_caveat", "fake_buffer_case", "binary_pres.bin", "X\x00Y\nZ\r\n", None, None, None, None, "policy", "success", "binary-mode-byte-preservation local observation", "")
add("c33_crlf_not_forced", "text_binary_caveat", "fake_file", "crlf.txt", "a\r\nb\r\n", None, None, None, None, "policy", "success", "CRLF-translation-not-forced", "portability")

# platform scope markers
add("c34_zos_not_tested", "portability_not_tested", "demo_stream", "zos.txt", "x", None, None, None, None, "policy", "skip", "zOS-record-files-not-tested", "portability")
add("c35_ebcdic_not_tested", "portability_not_tested", "synthetic_record", "ebcdic.txt", "x", None, None, None, None, "policy", "skip", "EBCDIC-conversion-not-tested", "portability")
add("c36_winpath_not_tested", "portability_not_tested", "toy_line", "winpath.txt", "x", None, None, None, None, "policy", "skip", "Windows-wide-paths-not-tested", "portability")
add("c37_posix_read_not_main", "portability_not_tested", "example_blob", "posix.txt", "x", None, None, None, None, "policy", "skip", "POSIX-read-not-main-implementation", "portability")
add("c38_fscanf_not_reader", "parser_design_scope", "sample_text", "scanf.txt", "x", None, None, None, None, "policy", "success", "fscanf-not-used-as-file-reader", "")
add("c39_path_bytes_vs_text", "path_encoding_caveat", "fake_config_line", "path.txt", "x", None, None, None, None, "policy", "success", "path-bytes-vs-text policy", "portability")
add("c40_locale_not_tested", "encoding_caveat", "demo_bytes", "locale.txt", "x", None, None, None, None, "policy", "skip", "locale-encoding-not-tested", "portability")

# wrapper
add("c41_wrapper_bytes_read", "wrapper_policy", "synthetic_newline_file", "wrap1.txt", "hello\n", 64, None, None, None, "wrapper", "success", "wrapper records bytes_read", "")
add("c42_wrapper_eof_error", "wrapper_policy", "toy_binary_blob", "wrap2.txt", "data", 64, None, None, None, "wrapper", "success", "wrapper records eof and error separately", "")
add("c43_wrapper_reject_partial", "wrapper_policy", "fictional_path_bytes", "wrap3.bin", "1234567", 64, None, None, None, "wrapper", "success", "wrapper rejects partial-record policy", "")
add("c44_wrapper_stream_chunk", "wrapper_policy", "fake_log_line", "wrap4.txt", "chunk\nchunk\n", 64, None, None, None, "wrapper", "success", "wrapper accepts streaming-chunk policy", "")

# naive footguns
add("c45_naive_feof_loop", "naive_file_io", "sample_short_read", "naive_feof.txt", "a\nb\n", 32, None, None, 32, "naive", "error", "naive-feof-loop", "naive_fail")
add("c46_naive_fread_nmemb", "naive_file_io", "demo_record_file", "naive_fread.bin", "12345678", 32, 4, 2, None, "naive", "error", "naive-fread-size-nmemb", "naive_fail")
add("c47_naive_strlen_binary", "naive_file_io", "synthetic_eof_case", "naive_strlen.bin", "A\x00BC", 32, None, None, 32, "naive", "error", "naive-fgets-strlen-binary", "naive_fail")

# scope markers
add("c48_external_platform", "portability_not_tested", "fake_buffer_case", "ext_plat.txt", "x", None, None, None, None, "policy", "skip", "external-platform-truth-not-tested", "portability")
add("c49_prod_parser", "parser_design_scope", "fake_file", "prod_parse.txt", "x", None, None, None, None, "policy", "skip", "production-parser-not-tested", "not_tested")
add("c50_safety_caveat", "safety_scope", "demo_stream", "safety.txt", "safe\n", None, None, None, None, "policy", "success", "safety_caveat marker", "")

# write fixture files
repo_root = pathlib.Path(".")
fixtures_dir = repo_root / "fixtures"
fixtures_dir.mkdir(exist_ok=True)
for c in cases:
    fname = c["fixture_name"]
    fpath = fixtures_dir / fname
    content = c["fixture_bytes"]
    # write as binary, latin1 preserves 0x00-0xff
    if isinstance(content, str):
        fpath.write_bytes(content.encode('latin1'))
    else:
        fpath.write_bytes(content)

# write cases.json (strip fixture_bytes to keep it small, keep len)
cases_json = []
for c in cases:
    cj = c.copy()
    cj["fixture_bytes_preview"] = (cj["fixture_bytes"][:40] + "...") if len(cj["fixture_bytes"]) > 40 else cj["fixture_bytes"]
    del cj["fixture_bytes"]
    cases_json.append(cj)

pathlib.Path("cases.json").write_text(json.dumps(cases_json, indent=2))
print(f"Wrote {len(cases)} cases to cases.json, fixtures in {fixtures_dir}/")
