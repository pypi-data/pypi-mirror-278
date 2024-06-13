from ...core import Utils, Logging, SynToolsError
import synapseclient as syn
from synapsis import Synapsis


class Move:
    def __init__(self, from_ids, to_id, dry_run=False):
        self._from_ids = from_ids
        self._to_id = to_id
        self._dry_run = dry_run
        self.to_container = None
        self.result = None

    async def execute(self):
        Logging.print_log_file_path()
        self.result = MoveResult(self._to_id)
        try:
            self.to_container = await Synapsis.Chain.get(self._to_id, downloadFile=False)

            if type(self.to_container) not in [syn.Project, syn.Folder]:
                self.result.errors.append('to-id must be a Synapse Project or Folder.')
                return self.result

            if self._dry_run:
                Logging.info('!!! Dry Run Only !!!', console=True)

            Logging.info('Moving to: {0} ({1})'.format(self.to_container.name, self.to_container.id), console=True)
            for from_id in self._from_ids:
                if from_id is None:
                    continue
                else:
                    from_id = from_id.strip()

                if Synapsis.is_synapse_id(from_id):
                    self.result.from_ids.append(from_id)
                else:
                    self.result.errors.append('Invalid Synapse ID: {0}'.format(from_id))

            for from_id in self.result.from_ids:
                await self._move(from_id)
            if self._dry_run:
                Logging.info('!!! Dry Run Only - Nothing Moved !!!', console=True)

        except Exception as ex:
            self.result.errors.append(str(ex))

        if self.result.errors:
            Logging.error('Finished with errors.')
            for error in self.result.errors:
                Logging.error(' - {0}'.format(error), console=True)
        if self.result.failed:
            Logging.error('Failed IDs:', console=True)
            for failed_syn_id in self.result.failed:
                Logging.error(' - {0}'.format(failed_syn_id), console=True)
        if self.result.moved:
            Logging.info('Successfully moved:', console=True)
            for syn_id in self.result.moved:
                Logging.info(' - {0}'.format(syn_id), console=True)

        return self.result

    async def _move(self, syn_id):
        try:
            move_entity = await Synapsis.Chain.get(syn_id)
            Logging.info('Moving: {0} ({1}) -> {2} ({3})'.format(move_entity.name, move_entity.id,
                                                                 self.to_container.name,
                                                                 self.to_container.id), console=True)
            if not self._dry_run:
                move_entity.parentId = self._to_id
                moved_entity = await Synapsis.Chain.store(move_entity)
                assert moved_entity.parentId == self._to_id
            else:
                # For dry-runs make sure a duplicate file/folder name doesn't exist.
                async for child in Synapsis.Chain.getChildren(self.to_container, includeTypes=['folder', 'file']):
                    if child['name'] == move_entity.name:
                        raise SynToolsError(
                            'An entity with the name: {0} already exists in: {1} ({2})'.format(move_entity.name,
                                                                                               self.to_container.name,
                                                                                               self.to_container.id))
                moved_entity = move_entity
            self.result.moved.append(moved_entity.id)
        except Exception as ex:
            self.result.failed.append(syn_id)
            self.result.errors.append('Error moving: {0} - {1}'.format(syn_id, ex))


class MoveResult:
    def __init__(self, to_id):
        self.from_ids = []
        self.to_id = to_id
        self.errors = []
        self.moved = []
        self.failed = []
