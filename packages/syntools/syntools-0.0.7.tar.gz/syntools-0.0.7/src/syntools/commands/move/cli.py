from .move import Move


def create(subparsers, parents):
    parser = subparsers.add_parser('move',
                                   parents=parents,
                                   help='Move Synapse entities from one container to another.')
    parser.add_argument('from_ids', metavar='from-ids', nargs='+',
                        help='The Synapse ID(s) to move from.')
    parser.add_argument('to_id', metavar='to-id', help='The Synapse container ID to move to.')
    parser.add_argument('-d', '--dry-run',
                        default=False,
                        action='store_true',
                        help='Dry run only. Do not move anything.')
    parser.set_defaults(_execute=execute)


async def execute(args):
    await Move(
        args.from_ids,
        args.to_id,
        dry_run=args.dry_run
    ).execute()
