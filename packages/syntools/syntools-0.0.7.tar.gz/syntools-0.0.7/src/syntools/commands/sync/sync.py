import os
import shutil
import synapseclient as syn
from datetime import datetime
from ...core import Utils, Logging, SynToolsError
from ..compare import Compare
from synapsis import Synapsis


class Sync:
    class OnUpdateActions:
        Update = 'update'
        Skip = 'skip'
        ALL = [Update, Skip]

    class OnDeleteActions:
        Delete = 'delete'
        Skip = 'skip'
        Move = 'move'
        ALL = [Delete, Skip, Move]

    def __init__(self, source, target,
                 excludes=None,
                 on_update=OnUpdateActions.Update,
                 on_delete=OnDeleteActions.Skip,
                 on_delete_move=None):
        self.source = source
        self.target = target
        self.excludes = excludes
        self.errors = []
        self._on_update = on_update.lower() if on_update else 'update'
        self._on_delete = on_delete.lower() if on_delete else 'skip'
        self._on_delete_move = on_delete_move

        self._source_is_remote = Synapsis.is_synapse_id(self.source)
        self._target_is_remote = Synapsis.is_synapse_id(self.target)

        if self._source_is_remote == self._target_is_remote:
            raise SynToolsError('Target and source must each be a Synapse ID and a local path.')

        if not self._source_is_remote:
            self.source = Utils.expand_path(self.source)

        if not self._target_is_remote:
            self.target = Utils.expand_path(self.target)

    async def execute(self):
        Logging.print_log_file_path()
        self.errors = []

        if self._source_is_remote:
            entity_id = self.source
            local_path = self.target
        else:
            entity_id = self.target
            local_path = self.source

        comparer = Compare(entity_id,
                           local_path,
                           excludes=self.excludes,
                           on_started=self.compare_on_started,
                           on_finished=self.compare_on_finished,
                           on_progress=self.compare_on_progress)
        await comparer.execute_async()

    async def compare_on_started(self, comparer):
        if self._source_is_remote:
            Logging.info(
                'Syncing: {0} ({1}) -> {2}'.format(comparer.entity.name, comparer.entity.id, comparer.local_path),
                console=True)
        else:
            Logging.info(
                'Syncing: {0} -> {1} ({2})'.format(comparer.local_path, comparer.entity.name, comparer.entity.id),
                console=True)

        if comparer.excludes:
            Logging.info('Excluding: {0}'.format(', '.join(comparer.excludes)), console=True)

    async def compare_on_finished(self, comparer):
        Logging.info('Run time: {0}'.format(comparer.end_time - (comparer.start_time or datetime.now())), console=True)

        if self.errors or comparer.errors:
            Logging.error('Finished with errors.', console=True)
            Logging.error(comparer.errors, console=True)
        else:
            Logging.info('Finished successfully.', console=True)

    async def compare_on_progress(self, comparer, compare_item):
        if not compare_item.is_excluded:
            if self._target_is_remote:
                await self._push(comparer, compare_item)
            else:
                await self._pull(comparer, compare_item)

    async def _pull(self, comparer, compare_item):
        can_handle_store = False
        item_type_label = 'DIRECTORY' if compare_item.is_dir else 'FILE'

        if compare_item.local_object is None:
            if self._on_update == Sync.OnUpdateActions.Update:
                can_handle_store = True
                action_label = 'CREATING' if compare_item.is_dir else 'DOWNLOADING'
            else:
                action_label = 'SKIPPING'

            Logging.error('[{0} NOT FOUND LOCALLY] {1}: {2} -> {3}'.format(item_type_label,
                                                                           action_label,
                                                                           compare_item.remote_path,
                                                                           compare_item.local_path), console=True)
        elif compare_item.remote_object is None:
            move_to_path = ''
            if self._on_delete == Sync.OnDeleteActions.Delete:
                action_label = 'DELETING'
                if compare_item.is_dir:
                    if os.path.isdir(compare_item.local_path):
                        shutil.rmtree(compare_item.local_path)
                else:
                    os.remove(compare_item.local_path)
            elif self._on_delete == Sync.OnDeleteActions.Move:
                action_label = 'MOVING'
                # TODO: Should this validation be moved to the constructor?
                if os.path.exists(self._on_delete_move) and not os.path.isdir(self._on_delete_move):
                    raise ValueError('Invalid on-delete-move path: {0}. Value must be a local directory path'.format(
                        self._on_delete_move))
                Utils.ensure_dirs(self._on_delete_move)
                dest = os.path.join(self._on_delete_move, os.path.basename(compare_item.local_path))
                shutil.move(compare_item.local_path, dest)
                move_to_path = ' to {0}'.format(dest)
            else:
                action_label = 'SKIPPING'

            Logging.error('[{0} NOT FOUND REMOTELY] {1}: {2}{3}'.format(item_type_label,
                                                                        action_label,
                                                                        compare_item.local_path,
                                                                        move_to_path), console=True)
        elif compare_item.is_file:
            if compare_item.local_object.size != compare_item.remote_object.size or \
                    compare_item.local_object.md5 != compare_item.remote_object.md5:
                if self._on_update == 'update':
                    can_handle_store = True
                    action_label = 'CREATING' if compare_item.is_dir else 'DOWNLOADING'
                else:
                    action_label = 'SKIPPING'
                Logging.error('[FILES DO NOT MATCH] {0}: {1} -> {2}'.format(action_label,
                                                                            compare_item.remote_path,
                                                                            compare_item.local_path), console=True)

        if can_handle_store:
            if compare_item.is_dir:
                Utils.ensure_dirs(compare_item.local_path)
            else:
                filehandle = await comparer.file_handle_view.get_filehandle(compare_item.remote_object.id)
                raise NotImplemented('todo')
                # await Synapsis.Chain.download_file(compare_item.remote_object.id,
                #                                      compare_item.local_path,
                #                                      filehandle,
                #                                      comparer.file_handle_view.get_filehandle)

    async def _push(self, comparer, compare_item):
        can_handle_store = False
        can_handle_delete = False
        item_type_label = 'DIRECTORY' if compare_item.is_dir else 'FILE'

        if compare_item.remote_object is None:
            if self._on_update == 'update':
                can_handle_store = True
                action_label = 'CREATING' if compare_item.is_dir else 'UPLOADING'
            else:
                action_label = 'SKIPPING'
            Logging.error('[{0} NOT FOUND REMOTELY] {1}: {2} -> {3}'.format(item_type_label,
                                                                            action_label,
                                                                            compare_item.local_path,
                                                                            compare_item.remote_path), console=True)
        elif compare_item.local_object is None:
            if self._on_delete == 'delete':
                can_handle_delete = True
                action_label = 'DELETING'
            elif self._on_delete == 'move':
                can_handle_delete = True
                action_label = 'MOVING'
            else:
                action_label = 'SKIPPING'

            Logging.error('[{0} NOT FOUND LOCALLY] {1}: {2}'.format(item_type_label,
                                                                    action_label,
                                                                    compare_item.remote_path), console=True)
        elif compare_item.is_file:
            if compare_item.local_object.size != compare_item.remote_object.size or \
                    compare_item.local_object.md5 != compare_item.remote_object.md5:
                if self._on_update == 'update':
                    can_handle_store = True
                    action_label = 'CREATING' if compare_item.is_dir else 'UPLOADING'
                else:
                    action_label = 'SKIPPING'
                Logging.error('[FILES DO NOT MATCH] {0}: {1} -> {2}'.format(action_label,
                                                                            compare_item.local_path,
                                                                            compare_item.remote_path), console=True)
        if can_handle_store:
            await self._store_remote(compare_item)
        elif can_handle_delete:
            await self._delete_remote(comparer, compare_item)

    async def _store_remote(self, compare_item):
        return False  # TODO: remove this after testing

        if compare_item.is_dir:
            await Synapsis.Chain.store(syn.Folder(name=compare_item.local_object.name,
                                                  parent=compare_item.remote_parent.id))
        else:
            await Synapsis.Chain.store(syn.File(name=compare_item.local_object.name,
                                                path=compare_item.local_object.path,
                                                parent=compare_item.remote_parent.id))

    async def _delete_remote(self, comparer, compare_item):
        return False  # TODO: remove this line after testing
        # TODO: Make this work.
        pass
