import asyncio
from datetime import datetime
from ...core import Utils, Logging, ResumableQueue, ThroughputTimer, SynToolsError, Env
from synapsis import Synapsis
import synapseclient as syn


class Copy:
    def __init__(self, from_id=None, to_id=None, only_children=False,
                 on_collision='update-if-different', skip_annotations=False, excludes=None,
                 restart=False, verbose=False):
        self.from_id = from_id
        self.to_id = to_id
        self.only_children = only_children
        self.resumable_queue = None
        self.errors = []
        self.on_collision = on_collision
        self.skip_annotations = skip_annotations
        self.excludes = []
        self.restart = restart
        self.verbose = verbose
        self.profile = None
        self.total_copied = 0
        self.throughput_timer = None

        for exclude in (excludes or []):
            if Synapsis.is_synapse_id(exclude):
                self.excludes.append(exclude.lower().strip())
            else:
                self.excludes.append(exclude)

    class Priorities:
        FILE = 1
        CONTAINER = 2
        CHILDREN = 3

    async def execute(self):
        start_time = datetime.now()
        Logging.print_log_file_path()
        aborted = False
        self.total_copied = 0
        self.throughput_timer = ThroughputTimer()
        try:
            if not Synapsis.is_synapse_id(self.from_id):
                self.add_error(error='Invalid Synapse FROM ID: {0}'.format(self.from_id))

            if not Synapsis.is_synapse_id(self.to_id):
                self.add_error(error='Invalid Synapse TO ID: {0}'.format(self.to_id))
            if self.errors:
                return self

            from_entity = await Synapsis.Chain.get(self.from_id, downloadFile=False)
            to_entity = await Synapsis.Chain.get(self.to_id, downloadFile=False)
            from_is_container = isinstance(from_entity, (syn.Project, syn.Folder))
            to_is_file = isinstance(to_entity, syn.File)
            if from_is_container and to_is_file:
                self.add_error(
                    error='Cannot copy container entity: {0} to a file: {1}.'.format(from_entity.id, to_entity.id))

            Logging.info('Copying from: {0} to: {1}'.format(from_entity.name, to_entity.name), console=True)

            if self.excludes:
                Logging.info('Excluding: {0}'.format(','.join(self.excludes)), console=True)

            self.resumable_queue = ResumableQueue.load(task_name='copy-{0}-{1}'.format(self.from_id, self.to_id),
                                                       reset=self.restart,
                                                       verbose=self.verbose)
            resume_copy = False
            if self.resumable_queue.can_resume:
                resume_copy = True
                Logging.info('Continuing existing copy operation.', console=True)
            else:
                if not self.resumable_queue.is_new:
                    Logging.warning(
                        'ResumableQueue status is: {0}, but does not have queued items. Resetting ResumableQueue'.format(
                            self.resumable_queue.status),
                        console=True)
                    self.resumable_queue.reset()

            self.profile = await Synapsis.Chain.getUserProfile()

            self.resumable_queue.set_started()
            self.throughput_timer.start()

            worker_count = Env.SYNTOOLS_COPY_WORKERS()
            Logging.info('Worker Count: {0}'.format(worker_count), console=False)
            workers = [asyncio.create_task(self._worker()) for _ in range(worker_count)]

            if resume_copy:
                queued_items = self.resumable_queue.queued.copy()
                for item in queued_items:
                    if self._copy_file.__name__ in item:
                        priority = self.Priorities.FILE
                    elif self._copy_container.__name__ in item:
                        priority = self.Priorities.CONTAINER
                    elif self._queue_children.__name__ in item:
                        priority = self.Priorities.CHILDREN
                    else:
                        raise SynToolsError('Invalid function: {0}'.format(item))
                    await self.resumable_queue.add_queued(priority, None, item=item)
                    self.print_stats()
            else:
                if from_is_container:
                    if self.only_children:
                        await self.resumable_queue.add_queued(self.Priorities.CHILDREN,
                                                              self._queue_children,
                                                              from_entity,
                                                              to_entity)
                    else:
                        await self.resumable_queue.add_queued(self.Priorities.CONTAINER,
                                                              self._copy_container,
                                                              from_entity,
                                                              to_entity)
                else:
                    await self.resumable_queue.add_queued(self.Priorities.FILE,
                                                          self._copy_file,
                                                          from_entity,
                                                          to_entity)

            await self.resumable_queue.join()
            for worker in workers:
                worker.cancel()

            self.resumable_queue.set_finished()
            print('')
        except asyncio.CancelledError:
            aborted = True
            print('')
            Logging.warning('User aborted. Shutting down...', console=True)
            for worker in workers:
                worker.cancel()
        except Exception as ex:
            self.add_error(error=ex)

        end_time = datetime.now()

        if self.resumable_queue and not self.resumable_queue.is_finished:
            if self.resumable_queue.has_queued:
                Logging.error('Queued items still present in ResumableQueue.', console=True)
            self.resumable_queue.save()

        Logging.info('Total processed: {0}'.format(self.throughput_timer.total_processed), console=True)
        Logging.info('Total Copied: {0}'.format(self.total_copied), console=True)

        if self.errors:
            if aborted:
                Logging.error('Aborted with errors.', console=True)
            else:
                Logging.error('Finished with errors.', console=True)

            for error in self.errors:
                Logging.error(' - {0}'.format(error), console=True)
        else:
            if aborted:
                Logging.info('Aborted.', console=True)
            else:
                Logging.info('Finished successfully.', console=True)

        Logging.info('Run time: {0}'.format(end_time - start_time), console=True)
        return self

    def print_stats(self, log_msg=None, log_func=None):
        if log_msg:
            Utils.print_inplace_reset()
            log_func(log_msg, console=self.verbose)

        stats = [
            'Processed: {0}'.format(self.throughput_timer.total_processed),
            'Copied: {0}'.format(self.total_copied),
            'Errors: {0}'.format(len(self.errors))
        ]
        if self.resumable_queue and self.throughput_timer:
            stats.append('Queued: {0}'.format(self.resumable_queue.queued_size))
            t_stats = self.throughput_timer.stats(self.resumable_queue.queued_size)
            if t_stats:
                stats.append(t_stats)
        Utils.print_inplace(', '.join(stats))

    async def _worker(self):
        while True:
            func, args, kwargs = await self.resumable_queue.get_queued(func_target=self)
            try:
                await func(*args, **kwargs)
                self.resumable_queue.remove_queued(func, *args, **kwargs)
            except Exception as ex:
                self._log_error('Worker Error', ex)
            finally:
                self.resumable_queue.task_done()
                self.print_stats()

    async def _copy_container(self, from_entity, to_entity):
        try:
            if not isinstance(from_entity, syn.Entity):
                from_entity = await Synapsis.Chain.get(from_entity, downloadFile=False)

            if not isinstance(to_entity, syn.Entity):
                to_entity = await Synapsis.Chain.get(to_entity, downloadFile=False)

            if not isinstance(from_entity, (syn.Project, syn.Folder)):
                raise SynToolsError('Expected project or folder but got: {0}'.format(from_entity))

            if not isinstance(to_entity, (syn.Project, syn.Folder)):
                raise SynToolsError('Cannot copy to: {0}, must be a Project or Folder'.format(to_entity))

            from_is_project = isinstance(from_entity, syn.Project)
            from_is_folder = isinstance(from_entity, syn.Folder)

            if from_is_folder:
                if self.can_skip(from_entity):
                    Logging.info('Skipping Folder: {0} ({1})'.format(from_entity.name, from_entity.id),
                                 console=self.verbose)
                else:
                    can_copy = True
                    folder_copy = await Synapsis.Chain.Utils.find_entity(from_entity.name, parent=to_entity)
                    if folder_copy is not None:
                        if self.on_collision == 'skip':
                            can_copy = False
                            Logging.info('Skipping Folder, already exists: {0} ({1})'.format(
                                from_entity.name,
                                folder_copy.id),
                                console=self.verbose)
                        elif self.on_collision == 'update-if-different':
                            if from_entity.name == folder_copy.name and \
                                    from_entity.annotations == folder_copy.annotations:
                                can_copy = False
                                self.throughput_timer.processed()
                                Logging.info(
                                    'Skipping Folder, folders match: {0} ({1}) -> {2} ({3})'.format(
                                        from_entity.name,
                                        from_entity.id,
                                        folder_copy.name,
                                        folder_copy.id),
                                    console=self.verbose)
                        elif self.on_collision == 'update':
                            can_copy = True

                    if can_copy:
                        annotations = None
                        if not self.skip_annotations:
                            annotations = from_entity.annotations

                        folder_copy = await Synapsis.Chain.store(syn.Folder(name=from_entity.name,
                                                                            parentId=Synapsis.id_of(to_entity),
                                                                            annotations=annotations))
                        self.total_copied += 1
                        self.add_copied(from_entity=from_entity, copy_entity=folder_copy)

                    await self.resumable_queue.add_queued(self.Priorities.CHILDREN,
                                                          self._queue_children,
                                                          from_entity,
                                                          folder_copy)
                    self.throughput_timer.processed()
            elif from_is_project:
                await self.resumable_queue.add_queued(self.Priorities.CHILDREN,
                                                      self._queue_children,
                                                      from_entity,
                                                      to_entity)
        except Exception as ex:
            self.add_error(from_entity=from_entity, copy_entity=to_entity, error=ex)

    async def _queue_children(self, from_entity, to_entity):
        try:
            async for child in Synapsis.Chain.getChildren(from_entity, includeTypes=["folder", "file"]):
                child_id = child['id']
                if Synapsis.ConcreteTypes.get(child).is_file:
                    await self.resumable_queue.add_queued(self.Priorities.FILE,
                                                          self._copy_file,
                                                          child_id,
                                                          to_entity)
                else:
                    await self.resumable_queue.add_queued(self.Priorities.CONTAINER,
                                                          self._copy_container,
                                                          child_id,
                                                          to_entity)
                self.print_stats()
        except Exception as ex:
            self.add_error(from_entity=from_entity, copy_entity=to_entity, error=ex)

    async def _copy_file(self, from_entity, to_entity):
        try:
            if not isinstance(from_entity, syn.Entity):
                from_entity = await Synapsis.Chain.get(from_entity, downloadFile=False)

            if not isinstance(to_entity, syn.Entity):
                to_entity = await Synapsis.Chain.get(to_entity, downloadFile=False)

            if not isinstance(from_entity, syn.File):
                raise SynToolsError('Expected file but got: {0}'.format(from_entity))

            if not isinstance(to_entity, (syn.Project, syn.Folder, syn.File)):
                raise SynToolsError('Cannot copy file to: {0}'.format(to_entity))

            to_parent_id = to_entity.parentId if isinstance(to_entity, syn.File) else to_entity
            from_file_handle = from_entity['_file_handle']

            if self.can_skip(from_entity):
                Logging.info('Skipping File: {0} ({1})'.format(from_entity.name, from_entity.id),
                             console=self.verbose)
            else:
                can_copy = True
                file_copy_id = await Synapsis.Chain.findEntityId(from_entity.name, parent=to_parent_id)
                if file_copy_id is not None:
                    if self.on_collision == 'skip':
                        can_copy = False
                        Logging.info('Skipping File, already exists: {0} ({1})'.format(
                            from_entity.name,
                            file_copy_id),
                            console=self.verbose)
                    elif self.on_collision == 'update-if-different':
                        file_copy = await Synapsis.Chain.get(file_copy_id, downloadFile=False)
                        to_file_handle = file_copy['_file_handle']
                        if from_file_handle['contentMd5'] == to_file_handle['contentMd5'] and \
                                from_file_handle['fileName'] == to_file_handle['fileName'] and \
                                from_entity.annotations == file_copy.annotations:
                            can_copy = False
                            Logging.info('Skipping File, files match: {0} ({1}) -> {2} ({3})'.format(
                                from_entity.name,
                                from_entity.id,
                                file_copy.name,
                                file_copy.id),
                                console=self.verbose)
                    elif self.on_collision == 'update':
                        can_copy = True

                if can_copy:
                    # CHECK: If the user created the file, copy the file by using fileHandleId else copy the fileHandle
                    if self.profile.ownerId == from_file_handle['createdBy']:
                        new_data_file_handle_id = from_entity.dataFileHandleId
                    else:
                        copied_file_handle = await Synapsis.Chain.Utils.copy_file_handles_batch(
                            [from_file_handle['id']], ["FileEntity"], [from_entity.id])
                        copy_result = copied_file_handle[0]
                        new_data_file_handle_id = copy_result['newFileHandle']['id']

                    annotations = None
                    if not self.skip_annotations:
                        annotations = from_entity.annotations
                    file_copy = await Synapsis.Chain.store(syn.File(
                        name=from_entity.name,
                        dataFileHandleId=new_data_file_handle_id,
                        parentId=Synapsis.id_of(to_parent_id),
                        annotations=annotations))
                    self.total_copied += 1
                    self.add_copied(from_entity=from_entity, copy_entity=file_copy)

            self.throughput_timer.processed()
        except Exception as ex:
            self.add_error(from_entity=from_entity, copy_entity=to_entity, error=ex)

    def add_copied(self, from_entity=None, from_name=None, copy_entity=None, copy_name=None, error=None):
        self.add_item('COPIED',
                      from_entity=from_entity,
                      from_name=from_name,
                      copy_entity=copy_entity,
                      copy_name=copy_name,
                      error=error)

    def add_error(self, from_entity=None, from_name=None, copy_entity=None, copy_name=None, error=None):
        self.add_item('ERROR',
                      from_entity=from_entity,
                      from_name=from_name,
                      copy_entity=copy_entity,
                      copy_name=copy_name,
                      error=error)

    def add_item(self, status, from_entity=None, from_name=None, copy_entity=None, copy_name=None, error=None):
        if isinstance(from_entity, syn.Entity):
            from_name = from_entity.name if from_name is None else from_name
            syn_type = Synapsis.ConcreteTypes.get(from_entity).name

        if isinstance(copy_entity, syn.Entity):
            copy_name = copy_entity.name if copy_name is None else copy_name

        from_id = Synapsis.id_of(from_entity)
        copy_id = Synapsis.id_of(copy_entity)

        segments = []
        if syn_type is not None:
            segments.append('{0}:'.format(syn_type))
        if from_id is not None and copy_id is not None:
            segments.append(
                '{0} ({1}) -> {2} ({3})'.format((from_name or 'Unknown'),
                                                from_id,
                                                (copy_name or 'Unknown'),
                                                copy_id))
        if error is not None:
            segments.append('Error: {0}'.format(error))
        log_message = ' '.join(segments)

        if status == 'COPIED':
            self.print_stats(log_msg='COPIED {0}'.format(log_message), log_func=Logging.info)
        elif status == 'ERROR':
            self.errors.append(log_message)
            self.print_stats(log_msg='ERROR {0}'.format(log_message), log_func=Logging.error)

    def can_skip(self, entity):
        if self.excludes:
            skip_values = [
                entity.id,
                entity.name
            ]
            for skip_value in skip_values:
                if skip_value in self.excludes:
                    return True

        return False
