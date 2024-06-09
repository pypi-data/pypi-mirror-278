from argparse import ArgumentParser, SUPPRESS

from . import __version__


PROG = __package__


class ArgParser(ArgumentParser):
    '''
    A custom command line parser used by the command line utility.
    '''

    def __init__(self) -> None:
        super().__init__(
            prog=PROG,
            argument_default=SUPPRESS,
        )
        self.add_arguments()

    def add_arguments(self) -> None:
        '''
        Equip the parser with all its arguments.
        '''

        self.add_argument(
            'source',
            action='extend',
            nargs='+',
            help="The file path(s) or literal Scuff to process.",
        )

        self.add_argument(
            '-j', '--to-json',
            dest='json',
            action='store_true',
            help="Convert `source` to JSON.",
        )

        self.add_argument(
            '-p', '--to-python',
            dest='py',
            action='store_true',
            help="Convert `source` to Python.",
        )

        self.add_argument(
            '-a', '--show-ast',
            dest='ast',
            action='store_true',
            help="Parse `source` and show its equivalent AST.",
        )

        self.add_argument(
            '--debug',
            action='store_true',
            help="Use debug mode. (Not implemented)",
        )

        self.add_argument(
            '-v', '--version',
            action='version',
            version=f"{__package__} {__version__}",
        )

    def parse_args(
        self,
        args: list[str] = None,
    ) -> dict[str]:
        '''
        Override :meth:`ArgumentParser.parse_args` and return command
        line options as a dict.
        '''
        opts = vars(super().parse_args(args))
        return opts

