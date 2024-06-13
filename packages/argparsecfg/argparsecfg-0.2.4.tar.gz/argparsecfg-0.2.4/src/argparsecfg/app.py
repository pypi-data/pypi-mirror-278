from __future__ import annotations

import argparse
from argparse import ArgumentParser, HelpFormatter
from dataclasses import is_dataclass
from functools import wraps
from inspect import getdoc, signature
from typing import Any, Callable, Optional, Sequence, Type

from argparsecfg.core import (
    ArgumentParserCfg,
    add_args_from_dc,
    create_dc_obj,
    create_parser,
)


def app(
    parser_cfg: ArgumentParserCfg | None = None,
    prog: str | None = None,
    usage: str | None = None,
    description: str | None = None,
    epilog: str | None = None,
    parents: Sequence[ArgumentParser] = [],  # type: ignore  - as at argparse
    formatter_class: Type[HelpFormatter] = HelpFormatter,
    prefix_chars: str = "-",
    fromfile_prefix_chars: str | None = None,
    argument_default: str | None = None,
    conflict_handler: str = "error",
    add_help: bool = True,
    allow_abbrev: bool = True,
    exit_on_error: bool = True,
):
    if parser_cfg is None:
        parser_cfg = ArgumentParserCfg(
            prog=prog,
            usage=usage,
            description=description,
            epilog=epilog,
            parents=parents,
            formatter_class=formatter_class,
            prefix_chars=prefix_chars,
            fromfile_prefix_chars=fromfile_prefix_chars,
            argument_default=argument_default,
            conflict_handler=conflict_handler,
            add_help=add_help,
            allow_abbrev=allow_abbrev,
            exit_on_error=exit_on_error,
        )
    # """Create app.
    # Simple variant - expecting function with one argument"""
    # to add - ags for argparse parser, ...

    def create_app(func: Callable[[Type[Any]], None]):
        sig = signature(func)
        params = [
            param.annotation
            for param in sig.parameters.values()
            if is_dataclass(param.annotation)
        ]
        app_cfg = params[0]

        @wraps(func)
        def parse_and_run(args: Optional[Sequence[str]] = None) -> None:
            parser = create_parser(parser_cfg)
            add_args_from_dc(parser, app_cfg)
            parsed_args = parser.parse_args(args)
            cfg = create_dc_obj(app_cfg, parsed_args)
            func(cfg)

        return parse_and_run

    return create_app


class App:
    subparsers: argparse.Action | None = None
    main_func: Callable[[Type[Any]], None]
    commands: dict[str, Callable[[Type[Any]], None]]
    configs: dict[str, Type[Any]]

    def __init__(
        self,
        parser_cfg: ArgumentParserCfg | None = None,
        prog: str | None = None,
        usage: str | None = None,
        description: str | None = None,
        epilog: str | None = None,
        parents: Sequence[ArgumentParser] = [],  # type: ignore  - as at argparse
        formatter_class: Type[HelpFormatter] = HelpFormatter,
        prefix_chars: str = "-",
        fromfile_prefix_chars: str | None = None,
        argument_default: str | None = None,
        conflict_handler: str = "error",
        add_help: bool = True,
        allow_abbrev: bool = True,
        exit_on_error: bool = True,
    ):
        if parser_cfg is None:
            self.parser = argparse.ArgumentParser(
                prog=prog,
                usage=usage,
                description=description,
                epilog=epilog,
                parents=parents,
                formatter_class=formatter_class,
                prefix_chars=prefix_chars,
                fromfile_prefix_chars=fromfile_prefix_chars,
                argument_default=argument_default,
                conflict_handler=conflict_handler,
                add_help=add_help,
                allow_abbrev=allow_abbrev,
                exit_on_error=exit_on_error,
            )
        else:
            self.parser = create_parser(parser_cfg)

    def main(self, func: Callable[[Type[Any]], None]):
        sig = signature(func)
        params = [
            param.annotation
            for param in sig.parameters.values()
            if is_dataclass(param.annotation)
        ]
        app_cfg = params[0]
        add_args_from_dc(self.parser, app_cfg)
        self.main_func = func
        self.main_cfg = app_cfg

        @wraps(func)
        def parse_and_run(args: Optional[Sequence[str]] = None) -> None:
            parsed_args = self.parser.parse_args(args)
            cfg = create_dc_obj(app_cfg, parsed_args)
            func(cfg)

        self.parse_and_run = parse_and_run
        return parse_and_run

    def command(self, func: Callable[[Type[Any]], None]):
        command_name = func.__name__
        if self.subparsers is None:
            self.subparsers = self.parser.add_subparsers(
                title="Commands", help="Available commands."
            )
            self.commands = {}
            self.configs = {}
        self.commands[command_name] = func
        help = getdoc(func)
        if help is not None:
            help = help.split("Args")[0].strip()
        command_parser = self.subparsers.add_parser(
            command_name,
            help=help,
            description=help,
        )
        command_parser.set_defaults(command=command_name)

        sig = signature(func)
        params = [
            param.annotation
            for param in sig.parameters.values()
            if is_dataclass(param.annotation)
        ]
        app_cfg = params[0]
        self.configs[command_name] = app_cfg

        add_args_from_dc(command_parser, app_cfg)

    def __call__(self, args: Optional[Sequence[str]] = None) -> None:
        # self.main_func(args)
        # self.parse_and_run(args)
        parsed_args = self.parser.parse_args(args)
        if hasattr(parsed_args, "command"):
            cfg = create_dc_obj(self.configs[parsed_args.command], parsed_args)
            self.commands[parsed_args.command](cfg)
        else:
            cfg = create_dc_obj(self.main_cfg, parsed_args)
            self.main_func(cfg)
