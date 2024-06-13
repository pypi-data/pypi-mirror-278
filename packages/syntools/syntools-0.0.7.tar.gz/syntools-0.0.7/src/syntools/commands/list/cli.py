from .list import List


def create(subparsers, parents):
    parser = subparsers.add_parser('list',
                                   parents=parents,
                                   help='List Synapse entities in one or more containers.')
    parser.add_argument('synapse_id', metavar='synapse-id', help='The Synapse container ID to list.')
    parser.add_argument('-t', '--type', help='Only list Folder or Files. Defaults to both if not set.',
                        choices=['folder', 'file'])
    parser.add_argument('-r', '--recursive', help='List all files and folders recursively.',
                        action='store_true',
                        default=False)
    parser.add_argument('-c', '--count', help='Only count the files and folders.',
                        action='store_true',
                        default=False)
    parser.add_argument('--file-size', help='Show the file sizes.',
                        action='store_true',
                        default=False)
    parser.set_defaults(_execute=execute)


async def execute(args):
    await List(
        args.synapse_id,
        include_types=args.type,
        recursive=args.recursive,
        count_only=args.count,
        with_filesize=args.file_size
    ).execute()
