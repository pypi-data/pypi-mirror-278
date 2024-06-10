import io
import sys
import time

from mgpy import mgstr


def test_log_print():
    hello_world = "Hello, world!"

    captured_output = io.StringIO()
    sys.stdout = captured_output
    mgstr.log_print(hello_world)
    sys.stdout = sys.__stdout__
    time_tuple = time.localtime()
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)

    assert f"[{time_string}]\t[Information]\t{hello_world}\n" == captured_output.getvalue()


def test_log_print_with_loglevel_error_and_no_time_format():
    hello_world = "Hello, world!"

    captured_output = io.StringIO()
    sys.stdout = captured_output
    mgstr.log_print(hello_world, mgstr.Loglevel.ERROR, None)
    sys.stdout = sys.__stdout__

    assert f"[ERROR]\t{hello_world}\n" == captured_output.getvalue()


def test_log_print_with_invalid_loglevel():
    hello_world = "Hello, world!"

    captured_output = io.StringIO()
    sys.stdout = captured_output
    mgstr.log_print(hello_world, [])
    sys.stdout = sys.__stdout__
    time_tuple = time.localtime()
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)

    assert f"[{time_string}]\t[Information]\t{hello_world}\n" == captured_output.getvalue()


def test_truncate_string():
    long_string = "long string is very long"

    truncated_string = mgstr.truncate_string(long_string, 11 + 3)

    assert "long string..." == truncated_string


def test_truncate_string_with_ellipsis():
    long_string = "long string is very long"

    truncated_string = mgstr.truncate_string(long_string, 11 + 1, "…")

    assert "long string…" == truncated_string

def test_truncate_string_with_empty_ellipsis():
    long_string = "long string is very long"

    truncated_string = mgstr.truncate_string(long_string, 11 + 0, "")

    assert "long string" == truncated_string

def test_truncate_string_with_too_short_length():
    short_string = "short string"

    truncated_string = mgstr.truncate_string(short_string, 2)

    assert "sh" == truncated_string


def test_insert_line_into_string():
    line_to_insert = "a new line"
    multi_line_string = "line 1\n" "line 2\n" "line 3\n"

    extended_string = mgstr.insert_line_into_string(line_to_insert, multi_line_string, 1)

    assert extended_string == "line 1\n" "a new line\n" "line 2\n" "line 3\n"


def test_insert_line_into_string_where_string_is_single_line():
    line_to_insert = "a new line"
    single_line_string = "line 1"

    extended_string = mgstr.insert_line_into_string(line_to_insert, single_line_string, 1)

    assert extended_string == "line 1\n" "a new line"


def test_insert_line_into_string_with_invalid_position():
    line_to_insert = "a new line"
    multi_line_string = "line 1\n" "line 2\n" "line 3\n"

    extended_string = mgstr.insert_line_into_string(line_to_insert, multi_line_string, 10)

    assert extended_string == "line 1\n" "line 2\n" "line 3\n" "a new line\n"


def test_insert_line_into_string_with_negative_position():
    line_to_insert = "a new line"
    multi_line_string = "line 1\n" "line 2\n" "line 3\n"

    extended_string = mgstr.insert_line_into_string(line_to_insert, multi_line_string, -1)

    assert extended_string == "line 1\n" "line 2\n" "a new line\n" "line 3\n"
