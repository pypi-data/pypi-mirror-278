from .copy import Copy


def create(subparsers, parents):
    parser = subparsers.add_parser('copy',
                                   parents=parents,
                                   help='Copy Synapse entities from one container to another.')
    parser.add_argument('from_id', metavar='from-id', help='The Synapse ID to copy from.')
    parser.add_argument('to_id', metavar='to-id', help='The Synapse ID to copy to.')
    parser.add_argument('--only-children',
                        help='Only copy the child items from the "FROM" entity and not the folder itself.',
                        default=False,
                        action='store_true'
                        )
    parser.add_argument('--on-collision',
                        help='How to handle items that exist in the TO location. Default: update-if-different',
                        choices=['skip', 'update', 'update-if-different'],
                        default='update-if-different')
    parser.add_argument('--skip-annotations',
                        help='Do not copy annotations.',
                        default=False,
                        action='store_true'
                        )
    parser.add_argument('-e', '--exclude',
                        action='append',
                        nargs='?',
                        help='Items to exclude from copying. Entity names or Synapse IDs.')
    parser.add_argument('-r', '--restart',
                        help='Force a copy restart if an in-progress copy exists.',
                        default=False,
                        action='store_true'
                        )
    parser.add_argument('-v', '--verbose',
                        help='Print status messages.',
                        default=False,
                        action='store_true'
                        )
    parser.set_defaults(_execute=execute)


async def execute(args):
    await Copy(
        from_id=args.from_id,
        to_id=args.to_id,
        only_children=args.only_children,
        on_collision=args.on_collision,
        skip_annotations=args.skip_annotations,
        excludes=args.exclude,
        restart=args.restart,
        verbose=args.verbose
    ).execute()
