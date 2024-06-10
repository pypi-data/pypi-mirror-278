from mgpy import mgnum


def test_generate_human_readable():
    ten_thousand_and_one = 10001
    one_point_five_billion = 1500000000

    ten_thousand_and_one_human_readable = mgnum.generate_human_readable_number(ten_thousand_and_one)
    one_point_five_billion_human_readable = mgnum.generate_human_readable_number(one_point_five_billion)

    assert "10k" == ten_thousand_and_one_human_readable
    assert "1.5G" == one_point_five_billion_human_readable


def test_generate_human_readable_german():
    one_point_five_billion = 1500000000
    german_suffixes = [" Tsd.", " Mio.", " Mrd.", " Bio.", " Brd."]
    german_separator = ","

    one_point_five_billion_human_readable = mgnum.generate_human_readable_number(one_point_five_billion, german_suffixes, german_separator)

    assert "1,5 Mrd." == one_point_five_billion_human_readable


def test_generate_human_readable_without_suffix():
    four_nine_nine = 499

    four_nine_nine_human_readable = mgnum.generate_human_readable_number(four_nine_nine)

    assert "499" == four_nine_nine_human_readable


def test_generate_human_readable_rounds_correct():
    nine_nine_nine = 999
    one_oh_oh_one = 1001

    nine_nine_nine_human_readable = mgnum.generate_human_readable_number(nine_nine_nine)
    one_oh_oh_one_human_readable = mgnum.generate_human_readable_number(one_oh_oh_one)

    assert "999" == nine_nine_nine_human_readable
    assert "1k" == one_oh_oh_one_human_readable
