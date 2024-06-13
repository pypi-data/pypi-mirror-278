import os
from ...core import Utils, Logging, EntityBundleWrapper, Env
import synapseclient as syn
import asyncio
from synapsis import Synapsis


class List:
    DEFAULT_INCLUDE_TYPES = 'folder,file'

    def __init__(self, synapse_id, include_types=None, recursive=True, count_only=False, with_filesize=False):
        self.start_id = synapse_id
        include_types = include_types if include_types else self.DEFAULT_INCLUDE_TYPES
        self.include_types = list(map(lambda t: Synapsis.ConcreteTypes.get(t), include_types.split(',')))
        self.recursive = recursive
        self.count_only = count_only
        self.with_filesize = with_filesize
        self.total_filesize = 0
        self.start_container = None
        self.queue = None
        self.result = None

    async def execute(self):
        Logging.print_log_file_path()
        self.result = ListResult(self.start_id)
        try:
            self.start_container = await Synapsis.Chain.get(self.start_id, downloadFile=False)

            if type(self.start_container) not in [syn.Project, syn.Folder]:
                self.result.errors.append('synapse-id must be a Synapse Project or Folder.')
                return self.result

            types = Synapsis.Chain.utils.map(self.include_types, lambda t: t.name + 's').Pipe.Call(
                lambda types: ','.join(types)).Result()
            Logging.info('Listing: {0} in {1} ({2})'.format(types, self.start_container.name, self.start_container.id),
                         console=True)

            self.queue = asyncio.Queue()
            producers = [asyncio.create_task(self._list(self.start_container, [self.start_container.name]))]
            if 'SYNTOOLS_LIST_WORKERS' in os.environ:
                worker_count = Env.SYNTOOLS_LIST_WORKERS()
            else:
                worker_count = Env.SYNTOOLS_LIST_WORKERS() if self.count_only else 1
            Logging.info('Worker Count: {0}'.format(worker_count), console=False)
            workers = [asyncio.create_task(self._worker()) for _ in range(worker_count)]
            await asyncio.gather(*producers)
            await self.queue.join()
            for worker in workers:
                worker.cancel()

        except Exception as ex:
            self.result.errors.append(str(ex))

        if self.count_only:
            Utils.print_inplace_reset()

        if self.result.errors:
            Logging.error('Finished with errors:', console=True)
            for error in self.result.errors:
                Logging.error(' - {0}'.format(error), console=True)
        else:
            folder_count = sum(i.type == 'Folder' for i in self.result.items)
            file_count = sum(i.type == 'File' for i in self.result.items)
            Logging.info('Total Items: {0}'.format(len(self.result.items)), console=True)
            Logging.info('Folders: {0}'.format(folder_count), console=True)
            Logging.info('Files: {0}'.format(file_count), console=True)
            if self.with_filesize:
                Logging.info('Total File Size: {0}'.format(self.total_filesize), console=True)
            Logging.info('Finished successfully.', console=True)

        return self.result

    async def _worker(self):
        while True:
            folder, paths = await self.queue.get()
            try:
                await self._list(folder.id, paths)
            except Exception as ex:
                self.result.errors.append(str(ex))
            finally:
                self.queue.task_done()

    async def _list(self, parent, paths):
        try:
            async for child in Synapsis.Chain.getChildren(parent, includeTypes=['folder', 'file']):
                child_type = Synapsis.ConcreteTypes.get(child)
                path = '/'.join(paths + [child['name']])
                synapse_item = ListResult.SynapseItem(child['id'], child_type.name, child['name'], path)

                if child_type in self.include_types:
                    if child_type.is_file and self.with_filesize:
                        file_bundle = await EntityBundleWrapper.fetch(synapse_item.id,
                                                                      include_file_handles=True,
                                                                      include_file_name=True)
                        synapse_item.content_size = file_bundle.content_size
                        synapse_item.filename = file_bundle.filename
                        self.total_filesize += synapse_item.content_size

                    self.result.items.append(synapse_item)
                    if self.count_only:
                        if len(self.result.items) % 100 == 0:
                            Utils.print_inplace('Counted {0} items...'.format(len(self.result.items)))
                    else:
                        file_info = ''
                        if child_type.is_file and self.with_filesize:
                            file_info = ' (Filename: {0} Size: {1})'.format(synapse_item.filename,
                                                                            synapse_item.content_size)
                        Logging.info(
                            '{0}: {1} {2}{3}'.format(synapse_item.type, synapse_item.id, synapse_item.path, file_info),
                            console=True)

                if child_type.is_folder and self.recursive:
                    await self.queue.put([synapse_item, paths + [synapse_item.name]])
        except Exception as ex:
            self.result.errors.append('Error listing: {0} - {1}'.format(parent, ex))


class ListResult:
    def __init__(self, synapse_id):
        self.synapse_id = synapse_id
        self.items = []
        self.errors = []

    class SynapseItem:
        def __init__(self, id, type, name, path, content_size=None, filename=None):
            self.id = id
            self.type = type
            self.name = name
            self.path = path
            self.content_size = content_size
            self.filename = filename
