from . import tools
from .cli import ArgParser

def main() -> None:
    '''
    Parse command line arguments, then format and print desired outputs.
    '''
    args = ArgParser().parse_args()

    conversions = {
        'ast': tools.dump,
        'json': tools.to_json,
        'py': tools.to_py,
    }
    sources = args.pop('source', None)
    for src in sources:
        for action in args:
            output = conversions[action](src)
            print(output)
            print()


if __name__ == '__main__':
    main()

