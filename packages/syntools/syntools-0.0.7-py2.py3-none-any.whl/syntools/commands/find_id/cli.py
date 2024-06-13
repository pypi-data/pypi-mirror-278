from .find_id import FindId


def create(subparsers, parents):
    parser = subparsers.add_parser('find-id',
                                   parents=parents,
                                   help='Find a Synapse ID by a Synapse path (e.g., MyProject/Folder/file.txt).')
    parser.add_argument('path', help='The Synapse path to find the ID for.')
    parser.set_defaults(_execute=execute)


async def execute(args):
    await FindId(
        args.path
    ).execute()
