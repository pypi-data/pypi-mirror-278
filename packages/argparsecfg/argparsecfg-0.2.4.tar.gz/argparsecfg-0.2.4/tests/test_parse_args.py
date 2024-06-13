import argparse
from dataclasses import dataclass
from unittest import mock

from argparsecfg.core import parse_args


@dataclass
class SimpleArg:
    arg_int: int
    arg_float: float = 0.0
    arg_str: str = ""


@mock.patch(
    "argparse.ArgumentParser.parse_args", return_value=argparse.Namespace(arg_int=1)
)
def test_parse_args(mock_args):  # type: ignore  pylint: disable=unused-argument
    cfg = parse_args(SimpleArg)
    assert cfg.arg_int == 1
    assert cfg.arg_float == 0.0
    assert cfg.arg_str == ""
