from .download import Download


def create(subparsers, parents):
    parser = subparsers.add_parser('download',
                                   parents=parents,
                                   help='Download folders and files from Synapse.')
    parser.add_argument('entity_id',
                        metavar='entity-id',
                        help='The ID of the Synapse entity to download (Project, Folder or File).')
    parser.add_argument('local_path',
                        metavar='local-path',
                        help='The local path to save the files to.')
    parser.add_argument('-e', '--exclude',
                        action='append',
                        nargs='?',
                        help='Items to exclude from download. Paths, names, or Synapse IDs.')
    parser.add_argument('-r', '--restart',
                        help='Force a download restart if an in-progress download exists.',
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
    await Download(
        args.entity_id,
        args.local_path,
        excludes=args.exclude,
        restart=args.restart,
        verbose=args.verbose
    ).execute()
