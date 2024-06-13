from .sync import Sync


def create(subparsers, parents):
    parser = subparsers.add_parser('sync',
                                   parents=parents,
                                   help='Sync folders and files to or from Synapse.')
    parser.add_argument('source', help='Synapse ID or local path to sync from.')
    parser.add_argument('target', help='Synapse ID or local path to sync to.')
    parser.add_argument('-e', '--exclude',
                        action='append',
                        nargs='?',
                        help='Items to exclude from comparison. Paths, names, or Synapse IDs.')
    parser.add_argument('-ou', '--on-update',
                        choices=Sync.OnUpdateActions.ALL,
                        default=Sync.OnUpdateActions.Update,
                        help='Action to be taken when a file needs to be updated.')
    parser.add_argument('-od', '--on-delete',
                        choices=Sync.OnDeleteActions.ALL,
                        default=Sync.OnDeleteActions.Skip,
                        help='Action to be taken when a file needs to be deleted.')
    parser.add_argument('-odm', '--on-delete-move',
                        default=None,
                        help='When --on-delete=move where to move the file to. Can be a local path or a Synapse ID.')
    parser.set_defaults(_execute=execute)


async def execute(args):
    await Sync(
        args.source,
        args.target,
        excludes=args.exclude,
        on_update=args.on_update,
        on_delete=args.on_delete,
        on_delete_move=args.on_delete_move
    ).execute()
