import argparse
from dataclasses import dataclass, field

from _pytest.capture import CaptureFixture

from argparsecfg.core import (
    ArgumentParserCfg,
    add_args_from_dc,
    add_argument_metadata,
    create_dc_obj,
    create_parser,
)
from argparsecfg.test_tools import (
    parsers_actions_diff,
    parsers_actions_equal,
    parsers_args_equal,
)


@dataclass
class ArgHelp:
    arg_int: int = field(metadata={"help": "simple help"})
    arg_float: float = field(
        default=0.0,
        metadata={"help": "simple help"},
    )
    arg_str: str = field(
        default="",
        metadata=add_argument_metadata(help="simple help"),
    )


def test_add_args_help():
    """test basic args with help"""
    # base parser
    parser_base = argparse.ArgumentParser()
    # parser_base.add_argument("--arg_int", type=int, required=True, help="simple help")
    parser_base.add_argument("--arg_int", type=int, help="simple help")  # Optional
    parser_base.add_argument("--arg_float", type=float, default=0.0, help="simple help")
    parser_base.add_argument("--arg_str", type=str, default="", help="simple help")

    # parser from cfg
    parser_cfg = ArgumentParserCfg()
    parser = create_parser(parser_cfg=parser_cfg)

    # add arguments - ArgHelp
    add_args_from_dc(parser, ArgHelp)
    assert parsers_args_equal(parser_base, parser)
    assert not parsers_actions_diff(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)
    assert parser_base.format_help() == parser.format_help()


def test_parser():
    """basic parser test create dataclass instance."""
    # create parser, add args
    parser = create_parser()
    add_args_from_dc(parser, ArgHelp)
    # parse
    args = parser.parse_args(["--arg_int", "10"])
    # create obj from parsed args
    dc_obj_parsed = create_dc_obj(ArgHelp, args)
    # obj same data from dataclass
    dc_obj_default = ArgHelp(arg_int=10)
    assert dc_obj_parsed == dc_obj_default


@dataclass
class ArgFlag:
    arg_1: int = field(default=1, metadata=add_argument_metadata("-a"))
    arg_2: int = field(default=1, metadata=add_argument_metadata(flag="b"))
    arg_3: int = field(default=1, metadata={"flag": "-c"})
    arg_4: int = field(default=1, metadata={"flag": "d"})


def test_add_flag():
    "test dc w flags"
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("-a", "--arg_1", type=int, default=1)
    parser_base.add_argument("-b", "--arg_2", type=int, default=1)
    parser_base.add_argument("-c", "--arg_3", type=int, default=1)
    parser_base.add_argument("-d", "--arg_4", type=int, default=1)

    parser = create_parser()
    add_args_from_dc(parser, ArgFlag)
    assert parsers_args_equal(parser_base, parser)
    assert not parsers_actions_diff(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)

    args = parser.parse_args([])
    # create obj from parsed args
    dc_obj_parsed = create_dc_obj(ArgFlag, args)
    # obj same data from dataclass
    dc_obj_default = ArgFlag()
    assert dc_obj_parsed == dc_obj_default


@dataclass
class ArgTypeDef:
    arg_1: int = field(default=1, metadata=add_argument_metadata(type=float))  # type: ignore  - for check error
    arg_2: int = field(default=1, metadata=add_argument_metadata(default=2.0))
    arg_3: int = field(default=1, metadata=add_argument_metadata(default=1.0))


def test_type_def(capsys: CaptureFixture[str]):
    "test dc wrong type and default at metadata"
    parser_base = argparse.ArgumentParser()
    parser_base.add_argument("--arg_1", type=int, default=1)
    parser_base.add_argument("--arg_2", type=int, default=1)
    parser_base.add_argument("--arg_3", type=int, default=1)

    parser = create_parser()
    add_args_from_dc(parser, ArgTypeDef)
    assert parsers_args_equal(parser_base, parser)
    assert parsers_actions_equal(parser_base, parser)

    captured = capsys.readouterr()
    out = captured.out
    assert "arg arg_1 type is <class 'int'>, but at metadata <class 'float'>" in out
    assert "default=1, but at metadata=2.0" in out

    args = parser.parse_args([])
    # create obj from parsed args
    dc_obj_parsed = create_dc_obj(ArgTypeDef, args)
    # obj same data from dataclass
    dc_obj_default = ArgTypeDef()
    assert dc_obj_parsed == dc_obj_default
