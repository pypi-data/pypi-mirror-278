# pylint: disable=protected-access
from dataclasses import dataclass, field

from _pytest.capture import CaptureFixture

from argparsecfg.core import (
    add_args_from_dc,
    add_argument_metadata,
    create_dc_obj,
    create_parser,
    field_argument,
)


def test_flag():
    """test add flag"""

    @dataclass
    class ArgFlag:
        arg_1: int = field_argument("--arg_1", flag="a")

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert "-a" in parser._option_string_actions
    assert "--arg_1" in parser._option_string_actions


def test_flag_2_useless(capsys: CaptureFixture[str]):
    """test add flag useless"""

    @dataclass
    class ArgFlag:
        arg_1: int = field_argument("-a", "--arg_1", flag="a")

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert "-a" in parser._option_string_actions
    assert "--arg_1" in parser._option_string_actions
    captured = capsys.readouterr()
    out = captured.out
    assert "got `flag` -a but args: ('-a', '--arg_1') given" in out


def test_flag_3_wrong_dc_name(capsys: CaptureFixture[str]):
    """test add flag different from dc name"""

    @dataclass
    class ArgFlag:
        arg_2: int = field_argument("-a", "--arg_1")

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert "-a" in parser._option_string_actions
    assert "--arg_1" not in parser._option_string_actions
    assert "--arg_2" in parser._option_string_actions
    captured = capsys.readouterr()
    out = captured.out
    assert "got `flag` --arg_1 but dc name is arg_2" in out


def test_flag_4_long_flag(capsys: CaptureFixture[str]):
    """test add flag different from dc name"""

    @dataclass
    class ArgFlag:
        arg_1: int = field_argument("-a", flag="--a1")

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert "-a" in parser._option_string_actions
    assert "--arg_1" not in parser._option_string_actions
    assert "--a1" in parser._option_string_actions
    captured = capsys.readouterr()
    out = captured.out
    assert out == ""
    args = parser.parse_args(["--a1", "1"])
    cfg = create_dc_obj(ArgFlag, args)
    assert cfg.arg_1 == 1


def test_wrong_dest(capsys: CaptureFixture[str]):
    """test add flag different from dc name"""

    @dataclass
    class ArgFlag:
        arg_1: int = field_argument("arg_2")

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert parser._actions[1].dest == "arg_1"
    captured = capsys.readouterr()
    out = captured.out
    assert "arg `dest` arg_2 but dc name is arg_1" in out


def test_metadata_wrong_default(capsys: CaptureFixture[str]):
    """test default different from dc default"""

    @dataclass
    class ArgFlag:
        arg_1: int = field(
            default=1,
            metadata=add_argument_metadata(default=2),
        )

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert parser._actions[1].default == 1
    captured = capsys.readouterr()
    out = captured.out
    assert "arg arg_1 default=1, but at metadata=2" in out


def test_metadata_wrong_default_none(capsys: CaptureFixture[str]):
    """test default different from dc None"""

    @dataclass
    class ArgFlag:
        arg_1: int = field(
            metadata=add_argument_metadata(default=2),
        )

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert parser._actions[1].default is None
    captured = capsys.readouterr()
    out = captured.out
    assert "arg arg_1 default=2 but dc default is None" in out


def test_metadata_wrong_type(capsys: CaptureFixture[str]):
    """test type different from dc type"""

    @dataclass
    class ArgFlag:
        arg_1: int = field_argument(
            default=1,
            type="float",
        )

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert parser._actions[1].default == 1
    assert parser._actions[1].type == int
    captured = capsys.readouterr()
    out = captured.out
    assert "arg arg_1 type is <class 'int'>, but at metadata float" in out
