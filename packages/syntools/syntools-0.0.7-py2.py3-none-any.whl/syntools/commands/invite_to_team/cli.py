from .invite_to_team import InviteToTeam


def create(subparsers, parents):
    parser = subparsers.add_parser('invite-to-team',
                                   parents=parents,
                                   help='Invite emails to a Synapse team.')
    parser.add_argument('team-id', help='The ID of the Synapse team.')
    parser.add_argument('emails', nargs='+',
                        help='Emails to invite')
    parser.set_defaults(_execute=execute)


async def execute(args):
    await InviteToTeam(
        args.team_id,
        args.emails
    ).execute()
