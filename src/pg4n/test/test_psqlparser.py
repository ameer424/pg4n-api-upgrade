"""Test PsqlParser."""

from ..psqlparser import PsqlParser


def test_parse_new_prompt() -> None:
    p = PsqlParser()

    case_trivial = \
        "\x1b[?2004hpgdb=> "
    assert p.parse_new_prompt(case_trivial) == \
        [" >="]

    case_mixed_results = \
        "\x1b[?2004l\r order_id | order_total_eur | customer_id \r\n----------+-----------------+-------------\r\n(0 rows)\r\n\r\n\x1b[?2004hpgdb=# "
    assert p.parse_new_prompt(case_mixed_results) == \
        [" #="]


def test_parse_new_prompt_and_rest() -> None:
    p = PsqlParser()

    case_trivial = \
        "\x1b[?2004hpgdb=> "
    assert p.parse_new_prompt_and_rest(case_trivial) == \
        ["", "\x1b[?2004hpgdb=> "]

    case_mixed_results = \
        "\x1b[?2004l\r order_id | order_total_eur | customer_id \r\n----------+-----------------+-------------\r\n(0 rows)\r\n\r\n\x1b[?2004hpgdb=# "
    assert p.parse_new_prompt_and_rest(case_mixed_results) == \
        ["\x1b[?2004l\r order_id | order_total_eur | customer_id \r\n----------+-----------------+-------------\r\n(0 rows)\r\n\r\n", "\x1b[?2004hpgdb=# "]


def test_parse_magical_return() -> None:
    p = PsqlParser()

    case_long_return = \
        "\r\x1b[16Ppgdb=# SELECT * FROM orders  WHERE order_total_eur = 0 AND order_tot\x08\r\n\x1b[?2004l\r"
    assert p.parse_magical_return(case_long_return) == \
        ["\rl4002?[\x1b\n\r"]


def test_parse_last_found_stmt() -> None:
    p = PsqlParser()

    case_trivial = \
        "psql (14.5)\nType \"help\" for help.\n\npgdb=# SELECT * FROM orders;"
    assert p.parse_last_found_stmt(case_trivial) == \
        "SELECT * FROM orders;"

    case_select_then_select = \
        "psql (14.5)\nType \"help\" for help.\n\npgdb=# SELECT * FROM orders;\npgdb=# SELECT * FROM orders WHERE order_total_eur = 0 AND order_total_eur = 100;"
    assert p.parse_last_found_stmt(case_select_then_select) == \
        "SELECT * FROM orders WHERE order_total_eur = 0 AND order_total_eur = 100;"

    # current unfixed bug case, needs to be fixed after mid-presentations:
#    case_select_then_insert = "psql (14.5)\nType \"help\" for help.\n\npgdb=# SELECT * FROM orders;\npgdb=# INSERT INTO orders VALUES (6, 6, 6);"
#    assert p.parse_last_found_stmt(case_select_then_insert) == \
#        ""
