# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import logging
import sys


# logging.basicConfig(level='DEBUG')

_initialized = False


def init(*args, **kwargs):
    global _initialized, _parser, _subparsers

    if not _initialized:
        _parser = ArgumentParser(*args, **kwargs)
        _subparsers = _parser.add_subparsers()

        _initialized = True

    return _parser


def make_verbosity_argument():
    _parser.add_argument('--verbosity', '-v', action='count', default=0,
                         help='Verbosity level (up to 4 v\'s)')


_first_level_commands = list()


class _CommandTreeLeaf(object):

    def __init__(self, name):
        self.name = name
        self.parser = None
        self.subparsers = None
        self.subcommands = list()

    def __repr__(self):
        return self.name


class _AbstractDecoration(object):

    def __init__(self):
        global _initialized

        if not _initialized:
            init()

        self._handler = None

    def _class(self):
        return self.__class__.__name__

    def __call__(self, handler):
        logging.debug(f'in {self._class()} __call__ (of {self.name})')
        logging.debug(f'args: {handler}')

        self._handler = handler

        import types
        if isinstance(handler, types.FunctionType):
            global current_command
            current_command.parser.set_defaults(handler=handler)
            return handler

        return self

    def __str__(self):
        return f'{self._class()} of {self.name}'


class Command(_AbstractDecoration):

    def __init__(self, name, *args, **kwargs):
        super().__init__()

        logging.debug('in {self._class()} __init__')
        logging.debug('name: ' + (name or '<root command>'))

        global _first_level_commands
        global current_command
        pre_existing, current_command = self._get_leaf_by_name(name)

        if not pre_existing:
            if name:
                current_command.parser = _subparsers.add_parser(name, *args, **kwargs)
            else:
                global _parser
                current_command.parser = _parser

        self.name = name

    def _get_leaf_by_name(self, name):
        global _first_level_commands
        for command in _first_level_commands:
            if command.name == name:
                return True, command

        newCommand = _CommandTreeLeaf(name)
        _first_level_commands.append(newCommand)
        return False, newCommand


class RootCommand(Command):

    def __init__(self, *args, **kwargs):
        logging.debug('in {self._class()} __init__')

        super().__init__(None)

        super().__call__(*args, **kwargs)


class SubCommand(_AbstractDecoration):

    def __init__(self, name, *args, **kwargs):
        super().__init__()

        logging.debug(f'in {self._class()} __init__')
        logging.debug(f'name: {name}')

        global current_command
        super_command = current_command
        pre_existing, current_command = self._get_leaf_by_name(name)

        if not pre_existing:
            if not super_command.subparsers:
                super_command.subparsers = super_command.parser.add_subparsers()
            current_command.parser = super_command.subparsers.add_parser(name, *args, **kwargs)

        self.name = name

    def _get_leaf_by_name(self, name):
        global current_command
        for command in current_command.subcommands:
            if command.name == name:
                return True, command

        newCommand = _CommandTreeLeaf(name)
        current_command.subcommands.append(newCommand)
        return False, newCommand


class Argument(_AbstractDecoration):

    def __init__(self, name, *args, **kwargs):
        super().__init__()

        logging.debug(f'in {self._class()} __init__')
        logging.debug('name: ' + str(name))

        global current_command
        current_command.parser.add_argument(name, *args, **kwargs)

        self.name = name


exception_handlers = list()


class ExceptionHandler(object):

    def __init__(self, method):
        exception_handlers.append(self)
        self.method = method

    def __call__(self, exception):
        return self.method(exception)


def _default_exception_handler(exception):
    if _args.get('verbosity', 0) == 4:
        raise exception

    logging.error(exception)

    return 1


def parse(*args, **kwargs):
    global _handler
    global _args

    parser_args = _parser.parse_args(*args, **kwargs)
    _args = dict(parser_args.__dict__)

    if 'handler' in _args:
        _handler = _args.pop('handler')
    else:
        _handler = _args

    return _args, _handler


def run():
    if _handler:
        try:
            kwargs = dict(_args)

            if 'verbosity' in kwargs:
                kwargs.pop('verbosity')

            return _handler(**kwargs)
        except Exception as e:
            if len(exception_handlers) == 0:
                result = _default_exception_handler(e)
            else:
                for handler in exception_handlers:
                    result = handler(e)

            sys.exit(result)
    else:
        _parser.print_help()
        return 0


def parse_and_run(*args, **kwargs):
    parse(*args, **kwargs)
    return run()


def finish():
    """
    No need to call this in production code, created for tests
    """
    global _first_level_commands, _initialized, _parser, _subparsers, current_command, _handler, _args
    _first_level_commands = list()
    _initialized = False
    _parser = None
    _subparsers = None
    current_command = None
    _handler = None
    _args = None
