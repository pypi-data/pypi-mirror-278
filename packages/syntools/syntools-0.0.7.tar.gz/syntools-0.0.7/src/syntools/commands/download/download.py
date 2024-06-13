import os
import asyncio
from datetime import datetime
import pathlib
from ...core import (Env, Utils, Logging, ResumableQueue, EntityBundleWrapper, ThroughputTimer,
                     FileSizeMismatchError, SynToolsError, WorkItemResult)
from synapsis import Synapsis


class Download:
    def __init__(self, starting_entity_id, download_path, excludes=None, restart=False, verbose=True):
        self.starting_entity_id = starting_entity_id
        self.download_path = Utils.expand_path(download_path)
        self.excludes = []
        self.restart = restart
        self.errors = []
        self.resumable_queue = None
        self.verbose = verbose
        self.total_processed = 0
        self.total_downloaded = 0
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
        self.errors = []
        aborted = False
        self.total_processed = 0
        self.total_downloaded = 0
        self.throughput_timer = ThroughputTimer()

        try:
            start_bundle = await EntityBundleWrapper.fetch(self.starting_entity_id,
                                                           include_entity=True,
                                                           include_entity_path=True,
                                                           include_file_handles=True)
            download_path = self.download_path
            if start_bundle.is_file and not os.path.isdir(download_path):
                if (os.path.isfile(download_path) or
                        os.path.basename(download_path) == start_bundle.filename or
                        pathlib.Path(download_path).suffix):
                    download_path = os.path.dirname(download_path)

            Utils.ensure_dirs(download_path)

            if not start_bundle.is_a(Synapsis.ConcreteTypes.PROJECT_ENTITY,
                                     Synapsis.ConcreteTypes.FOLDER_ENTITY,
                                     Synapsis.ConcreteTypes.FILE_ENTITY):
                self._log_error('Starting entity must be a Project, Folder, or File.')
                return self

            Logging.info('Downloading: {0} ({1}) to {2}'.format(start_bundle.name,
                                                                start_bundle.id,
                                                                download_path), console=True)

            if self.excludes:
                Logging.info('Excluding: {0}'.format(','.join(self.excludes)), console=True)

            if Env.SYNTOOLS_SYN_GET_DOWNLOAD():
                Logging.info('Using synapseclient.get for downloads.', console=True)

            self.resumable_queue = ResumableQueue.load(
                task_name='download-{0}'.format(self.starting_entity_id),
                uniq_suffix=download_path,
                reset=self.restart,
                verbose=self.verbose)

            resume = False
            if self.resumable_queue.can_resume:
                resume = True
                Logging.info('Continuing existing download operation.', console=True)
            else:
                if not self.resumable_queue.is_new:
                    Logging.warning(
                        'ResumableQueue status is: {0}, but does not have queued items. Resetting ResumableQueue'.format(
                            self.resumable_queue.status),
                        console=True)
                    self.resumable_queue.reset()

            self.resumable_queue.set_started()
            self.throughput_timer.start()

            worker_count = Env.SYNTOOLS_DOWNLOAD_WORKERS()
            Logging.info('Worker Count: {0}'.format(worker_count), console=False)
            workers = [asyncio.create_task(self._worker()) for _ in range(worker_count)]

            if resume:
                queued_items = self.resumable_queue.queued.copy()
                for item in queued_items:
                    if self._download_file.__name__ in item:
                        priority = self.Priorities.FILE
                    elif self._download_container.__name__ in item:
                        priority = self.Priorities.CONTAINER
                    elif self._queue_children.__name__ in item:
                        priority = self.Priorities.CHILDREN
                    else:
                        raise SynToolsError('Invalid function: {0}'.format(item))
                    await self.resumable_queue.add_queued(priority, None, item=item)
                    self.print_stats()
            else:
                if start_bundle.is_file:
                    await self.resumable_queue.add_queued(self.Priorities.FILE,
                                                          self._download_file,
                                                          start_bundle,
                                                          download_path)
                else:
                    await self.resumable_queue.add_queued(self.Priorities.CONTAINER,
                                                          self._download_container,
                                                          start_bundle,
                                                          download_path)

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
            self._log_error('Execute Error', error=ex)

        end_time = datetime.now()

        if self.resumable_queue and not self.resumable_queue.is_finished:
            if self.resumable_queue.has_queued:
                Logging.error('Queued items still present in ResumableQueue.', console=True)
            self.resumable_queue.save()

        Logging.info('Total Processed: {0}'.format(self.total_processed), console=True)
        Logging.info('Total Downloaded: {0}'.format(self.total_downloaded), console=True)

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
            'Processed: {0}'.format(self.total_processed),
            'Downloaded: {0}'.format(self.total_downloaded),
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
                total_processed = 0
                max_tries = 10
                attempt = 0
                while attempt < max_tries:
                    attempt += 1
                    if attempt > 1:
                        Logging.info(
                            'Retrying: {0}({1}{2})'.format(
                                func.__name__,
                                ', '.join(args),
                                ', '.join('{0}={1}'.format(key, value) for key, value in kwargs.items())
                            ),
                            console=self.verbose
                        )
                    func_result = await func(*args, **kwargs)
                    if func_result.error is None:
                        total_processed = func_result.total_processed
                        break
                    else:
                        max_tries = func_result.retry_max
                        if func_result.can_retry and attempt < max_tries:
                            sleep_dur = attempt * func_result.retry_modifier
                            Logging.info(
                                '{0}. Attempting Retry: {1}({2}{3}) in {4} seconds.'.format(
                                    func_result.error.original_message,
                                    func.__name__,
                                    ', '.join(args),
                                    ', '.join('{0}={1}'.format(key, value) for key, value in kwargs.items()),
                                    sleep_dur
                                ),
                                console=self.verbose
                            )
                            await asyncio.sleep(sleep_dur)
                        else:
                            raise func_result.error
            except Exception as ex:
                total_processed = 1
                self._log_error(None, ex)
            finally:
                for _ in range(total_processed):
                    self.total_processed += 1
                    self.throughput_timer.processed()
                self.resumable_queue.remove_queued(func, *args, **kwargs)
                self.resumable_queue.task_done()
                self.print_stats()

    async def _download_container(self, entity_bundle, local_path):
        result = WorkItemResult()
        full_remote_path = None
        local_abs_full_path = None
        try:
            if isinstance(entity_bundle, str):
                entity_bundle = await EntityBundleWrapper.fetch(entity_bundle,
                                                                include_entity=True,
                                                                include_entity_path=True,
                                                                include_has_children=True)

            if not entity_bundle.is_a(Synapsis.ConcreteTypes.PROJECT_ENTITY, Synapsis.ConcreteTypes.FOLDER_ENTITY):
                raise SynToolsError('Expected project or folder but got: {0}'.format(entity_bundle.entity_type),
                                    can_retry=False)

            full_remote_path = entity_bundle.synapse_path

            if entity_bundle.is_folder:
                local_abs_full_path = os.path.join(local_path, entity_bundle.name)
                if self.can_skip(entity_bundle, local_abs_full_path):
                    Logging.info('Skipping Folder: {0} ({1})'.format(full_remote_path, entity_bundle.id),
                                 console=self.verbose)
                else:
                    if os.path.isdir(local_abs_full_path):
                        Logging.info('Folder Exists: {0} ({1}) -> {2}'.format(full_remote_path,
                                                                              entity_bundle.id,
                                                                              local_abs_full_path), self.verbose)
                    else:
                        Logging.info('Folder: {0} ({1}) -> {2}'.format(full_remote_path,
                                                                       entity_bundle.id,
                                                                       local_abs_full_path), self.verbose)
                        if not os.path.isfile(local_abs_full_path):
                            Utils.ensure_dirs(local_abs_full_path)
                            self.total_downloaded += 1

                    if entity_bundle.has_children:
                        await self.resumable_queue.add_queued(self.Priorities.CHILDREN,
                                                              self._queue_children,
                                                              entity_bundle.id,
                                                              local_abs_full_path)

                result.result = local_abs_full_path
                result.total_processed += 1
            else:
                await self.resumable_queue.add_queued(self.Priorities.CHILDREN,
                                                      self._queue_children,
                                                      entity_bundle.id,
                                                      local_path)
                result.result = True
        except Exception as ex:
            msg = 'Failed to Download Container:'
            failed_id = entity_bundle.id if isinstance(entity_bundle, EntityBundleWrapper) else entity_bundle
            if full_remote_path:
                msg += ' {0} ({1})'.format(full_remote_path, failed_id)
            else:
                msg += ' {0}'.format(failed_id)

            if local_abs_full_path:
                msg += ' -> {0}'.format(local_abs_full_path)
            result.error = SynToolsError(msg, can_retry=True, child_error=ex)

        return result

    async def _queue_children(self, entity_id, local_path):
        result = WorkItemResult()
        try:
            file_ids = []
            folder_ids = []

            async def queue_items(max_files=None, max_folders=None):
                can_queue_files = True
                can_queue_folders = True

                if max_files is not None and len(file_ids) <= max_files:
                    can_queue_files = False

                if max_folders is not None and len(folder_ids) <= max_folders:
                    can_queue_folders = False

                if can_queue_files:
                    for file_id in file_ids:
                        await self.resumable_queue.add_queued(self.Priorities.FILE,
                                                              self._download_file,
                                                              file_id,
                                                              local_path)
                    file_ids.clear()

                if can_queue_folders:
                    for folder_id in folder_ids:
                        await self.resumable_queue.add_queued(self.Priorities.CONTAINER,
                                                              self._download_container,
                                                              folder_id,
                                                              local_path)
                    folder_ids.clear()

                if can_queue_files or can_queue_folders:
                    self.print_stats()

            async for child in Synapsis.Chain.getChildren(entity_id,
                                                          includeTypes=["folder", "file"],
                                                          sortBy='MODIFIED_ON',
                                                          sortDirection='DESC'):
                child_id = child['id']
                if Synapsis.ConcreteTypes.get(child).is_file:
                    file_ids.append(child_id)
                else:
                    folder_ids.append(child_id)
                await queue_items(max_files=5, max_folders=100)

            await queue_items()
            result.result = True
        except Exception as ex:
            result.error = SynToolsError(
                'Failed to get folders and files for: {0}'.format(entity_id),
                can_retry=True,
                child_error=ex
            )
        return result

    async def _download_file(self, entity_bundle, local_path):
        result = WorkItemResult()
        full_remote_path = None
        download_path = None
        try:
            if local_path != Utils.real_path(local_path):
                Logging.info(
                    'Changing local path: {0} to real path: {1}'.format(local_path, Utils.real_path(local_path)))
                local_path = Utils.real_path(local_path)

            if isinstance(entity_bundle, str):
                entity_bundle = await EntityBundleWrapper.fetch(entity_bundle,
                                                                include_entity=True,
                                                                include_entity_path=True,
                                                                include_file_handles=True)
            if not entity_bundle.is_file:
                raise SynToolsError('Expected file but got: {0}'.format(entity_bundle.entity_type), can_retry=False)

            full_remote_path = entity_bundle.synapse_path
            download_path = Utils.real_path(os.path.join(local_path, entity_bundle.filename))

            if self.can_skip(entity_bundle, download_path):
                result.result = download_path
                Logging.info('Skipping File: {0} ({1})'.format(full_remote_path, entity_bundle.id),
                             console=self.verbose)
            else:
                remote_md5 = entity_bundle.content_md5
                remote_content_size = entity_bundle.content_size
                # NOTE: For ExternalFileHandles the size and MD5 data will not be present.
                is_unknown_size = remote_content_size is None

                can_download = True

                if is_unknown_size:
                    Logging.info(
                        'External File: {0}, cannot determine changes. Force downloading.'.format(full_remote_path),
                        console=self.verbose)
                elif os.path.isfile(download_path):
                    local_size = os.path.getsize(download_path)
                    if local_size == remote_content_size:
                        # Only check the md5 if the file sizes match.
                        # This way we can avoid MD5 checking for partial downloads and changed files.
                        local_md5 = await Synapsis.Chain.Utils.md5sum(download_path)
                        if local_md5 == remote_md5:
                            can_download = False
                            Logging.info(
                                'File is current: {0} ({1}) -> {2}'.format(full_remote_path,
                                                                           entity_bundle.id,
                                                                           download_path), console=self.verbose)
                if can_download:
                    if Env.SYNTOOLS_SYN_GET_DOWNLOAD():
                        downloaded_file = await Synapsis.Chain.get(entity_bundle.id,
                                                                   downloadFile=True,
                                                                   downloadLocation=local_path,
                                                                   ifcollision='overwrite.local')
                        downloaded_path = downloaded_file.path
                    else:
                        downloaded_path = await Synapsis.Chain.Synapse._downloadFileHandle(
                            entity_bundle.data_file_handle_id,
                            entity_bundle.id,
                            'FileEntity',
                            local_path,
                            retries=Env.SYNTOOLS_DOWNLOAD_RETRIES())
                        if downloaded_path is None or downloaded_path.strip() == '':
                            raise SynToolsError('Download error.', can_retry=True)

                    downloaded_real_path = Utils.real_path(downloaded_path)

                    if (entity_bundle.file_handle_concrete_type.is_EXTERNALFILEHANDLE and
                            downloaded_real_path != download_path):
                        os.rename(downloaded_real_path, download_path)
                        downloaded_real_path = Utils.real_path(download_path)

                    if downloaded_real_path != download_path:
                        if os.path.exists(download_path):
                            os.remove(download_path)
                        raise SynToolsError(
                            'Downloaded path: {0} does not match expected path: {1}. Downloaded file deleted.'.format(
                                downloaded_real_path,
                                download_path),
                            can_retry=False
                        )

                    downloaded_size = os.path.getsize(download_path)
                    if not is_unknown_size and downloaded_size != entity_bundle.content_size:
                        if os.path.exists(download_path):
                            os.remove(download_path)
                        raise FileSizeMismatchError(
                            'Downloaded size: {0} does not match expected size: {1}. Downloaded file deleted.'.format(
                                downloaded_size,
                                entity_bundle.content_size),
                            can_retry=False
                        )

                    self.total_downloaded += 1
                    result.result = downloaded_real_path
                    Logging.info(
                        'File  : {0} ({1}) -> {2} ({3})'.format(full_remote_path,
                                                                entity_bundle.id,
                                                                download_path,
                                                                Utils.pretty_size(downloaded_size)),
                        console=self.verbose)
        except Exception as ex:
            msg = 'Failed to Download File:'
            failed_id = entity_bundle.id if isinstance(entity_bundle, EntityBundleWrapper) else entity_bundle
            if full_remote_path:
                msg += ' {0} ({1})'.format(full_remote_path, failed_id)
            else:
                msg += ' {0}'.format(failed_id)

            if download_path:
                msg += ' -> {0}'.format(download_path)
            else:
                msg += ' -> {0}'.format(local_path)

            result.error = SynToolsError(msg, can_retry=True, child_error=ex)

        if result.error is None:
            result.total_processed += 1
        return result

    def can_skip(self, bundle, local_path):
        if self.excludes:
            skip_values = [
                bundle.id,
                bundle.name,
                bundle.synapse_path,
                local_path,
                os.path.dirname(local_path),
                os.path.basename(local_path)
            ]
            for skip_value in skip_values:
                if skip_value in self.excludes:
                    return True

        return False

    def _log_error(self, msg, error=None):
        if error:
            log_msg = '. '.join(filter(None, [msg, str(error)]))
            self.errors.append(log_msg)
            self.print_stats(log_msg="ERROR: {0}".format(log_msg), log_func=Logging.exception)
        else:
            self.errors.append(msg)
            self.print_stats(log_msg=msg, log_func=Logging.error)
