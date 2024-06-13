import time
from ...core import Logging
from synapsis import Synapsis


class InviteToTeam:
    def __init__(self, team_id, emails, dry_run=False):
        self._team_id = team_id
        self._emails = emails
        self._dry_run = dry_run
        self.result = None
        self.team = None

    async def execute(self):
        Logging.print_log_file_path()
        self.result = InviteToTeamResult(self._team_id)
        try:
            self.team = await Synapsis.Chain.getTeam(self._team_id)
            Logging.info('Inviting to team: {0}'.format(self.team.name), console=True)

            for email in self._emails:
                if email is None:
                    continue
                else:
                    email = email.strip()
                if '@' in email:
                    self.result.emails.append(email)
                else:
                    self.result.errors.append('Invalid email address: {0}'.format(email))

            for email in self.result.emails:
                # Sleep to avoid throttling on Synapse's end.
                time.sleep(3)
                self._invite_email(email)

        except Exception as ex:
            self.result.errors.append(str(ex))

        if self.result.errors:
            Logging.error('Finished with errors.')
            for error in self.result.errors:
                Logging.error(' - {0}'.format(error), console=True)
        if self.result.failed:
            Logging.error('Failed:', console=True)
            for failed_syn_id in self.result.failed:
                Logging.error(' - {0}'.format(failed_syn_id), console=True)

        return self.result

    def _invite_email(self, email):
        try:
            Logging.info('Inviting: {0}'.format(email), console=True)
            if not self._dry_run:
                Synapsis.Utils.invite_to_team(self.team, email)
            self.result.sent.append(email)
        except Exception as ex:
            self.result.failed.append(email)
            self.result.errors.append('Error inviting: {0} - {1}'.format(email, ex))


class InviteToTeamResult:
    def __init__(self, team_id):
        self.team_id = team_id
        self.errors = []
        self.emails = []
        self.sent = []
        self.failed = []
