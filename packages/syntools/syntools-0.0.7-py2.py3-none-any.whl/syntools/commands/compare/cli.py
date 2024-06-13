from .compare import Compare


def create(subparsers, parents):
    parser = subparsers.add_parser('compare',
                                   parents=parents,
                                   help='Compare two Synapse entities or Synapse entities against a local directory and/or files.')
    parser.add_argument('entity_id', metavar='entity-id',
                        help='The ID of the Synapse entity to compare.')
    parser.add_argument('local_path', metavar='local-path',
                        help='The local path or Synapse ID to compare against.')
    parser.add_argument('-e', '--exclude',
                        help='Items to exclude from comparison. Paths, names, or Synapse IDs.',
                        action='append', nargs='?')
    parser.set_defaults(_execute=execute)


async def execute(args):
    await Compare(
        args.entity_id,
        args.local_path,
        excludes=args.exclude
    ).execute()
