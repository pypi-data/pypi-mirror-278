import os
from datetime import datetime
import asyncio
import synapseclient as syn
from synapsis import Synapsis
from ...core import Utils, SynapseItem, Logging, Env


class Compare:

    def __init__(self, starting_entity_id, compare_path_or_id, excludes=None):
        self._starting_entity_id = starting_entity_id
        self._compare_path_or_id = compare_path_or_id
        self._is_remote_compare = Synapsis.is_synapse_id(self._compare_path_or_id)
        self._excludes = []
        for exclude in (excludes or []):
            if Synapsis.is_synapse_id(exclude):
                self._excludes.append(exclude.lower().strip())
            else:
                self._excludes.append(exclude)

        self.queue = None
        self.start_time = None
        self.end_time = None
        self.result = None
        self.total_items_found = 0
        self.left_comparables = {}

    async def execute(self):
        Logging.print_log_file_path()
        self.result = CompareResult(self._starting_entity_id, self._compare_path_or_id)
        self.total_items_found = 0
        self.left_comparables = {}

        self.start_time = datetime.now()
        await self._execute_async()
        self.end_time = datetime.now()

        Logging.info('', console=True)
        Logging.info('Run time: {0}'.format(self.end_time - (self.start_time or datetime.now())), console=True)
        Logging.info('Found {0} items to compare.'.format(self.total_items_found), console=True)
        Logging.info('Compared {0} items.'.format(self.result.total_compared), console=True)

        success = not self.result.errors and not self.result.missing and not self.result.not_equal
        if success:
            Logging.info('Finished successfully.', console=True)
        else:
            if self.result.missing:
                Logging.warning('Found {0} missing items.'.format(len(self.result.missing)), console=True)
            if self.result.not_equal:
                Logging.warning('Found {0} mismatched items.'.format(len(self.result.not_equal)), console=True)

            if self.result.errors:
                Logging.error('Finished with errors.', console=True)
                for error in self.result.errors:
                    Logging.error(' - {0}'.format(error), console=True)

        return self.result

    async def _execute_async(self):
        try:
            start_entity = await Synapsis.Chain.get(self._starting_entity_id, downloadFile=False)
            compare_entity = None
            if self._is_remote_compare:
                compare_entity = await Synapsis.Chain.get(self._compare_path_or_id, downloadFile=False)

            if not self.validate_for_compare(start_entity, compare_entity):
                return

            start_entity = SynapseItem(start_entity)
            start_entity_is_file = start_entity.is_file
            if self._is_remote_compare:
                compare_entity = SynapseItem(compare_entity)
                start_entity.compare_item = compare_entity

            if self._is_remote_compare:
                Logging.info('Comparing: {0} ({1}) to {2} ({3})'.format(start_entity.name,
                                                                        start_entity.id,
                                                                        compare_entity.name,
                                                                        compare_entity.id),
                             console=True)
            else:
                Logging.info('Comparing: {0} ({1}) to {2}'.format(start_entity.name,
                                                                  start_entity.id,
                                                                  self._compare_path_or_id), console=True)

            if self._excludes:
                Logging.info('Excluding: {0}'.format(','.join(self._excludes)), console=True)

            Logging.info('Gathering Compare Items...', console=True)

            self.queue = asyncio.Queue()
            compare_path_or_id = '' if compare_entity is not None else self._compare_path_or_id
            self._add_comparable(start_entity, self.left_comparables)
            producers = [asyncio.create_task(self._process_children(start_entity, compare_path_or_id, compare_entity))]
            worker_count = Env.SYNTOOLS_COMPARE_WORKERS()
            Logging.info('Worker Count: {0}'.format(worker_count), console=False)
            workers = [asyncio.create_task(self._worker()) for _ in range(worker_count)]
            await asyncio.gather(*producers)
            await self.queue.join()
            for worker in workers:
                worker.cancel()

            print('')
            Logging.info('Starting Compare Process...', console=True)
            if self._is_remote_compare:
                if start_entity_is_file:
                    parent = await Synapsis.Chain.get(start_entity.parentId)
                    parent = SynapseItem(parent)
                    await self._compare_remote(parent)
                else:
                    await self._compare_remote(start_entity)
            else:
                if start_entity_is_file:
                    parent = await Synapsis.Chain.get(start_entity.parentId)
                    parent = SynapseItem(parent)
                    await self._compare_local(parent, compare_path_or_id)
                else:
                    await self._compare_local(start_entity, compare_path_or_id)

        except Exception as ex:
            self._log_error(ex)

    def validate_for_compare(self, start_entity, compare_entity=None):
        if type(start_entity) not in [syn.Project, syn.Folder, syn.File]:
            self._log_error('Starting entity must be a Project, Folder, or File.')
            return False
        start_entity_is_file = isinstance(start_entity, syn.File)

        if self._is_remote_compare:
            if compare_entity is None:
                self._log_error('Compare entity does not exist: {0}'.format(self._compare_path_or_id))
                return False
            else:
                compare_entity_is_file = isinstance(compare_entity, syn.File)
                if start_entity_is_file and not compare_entity_is_file:
                    self._log_error('Starting entity and compare entity must both be a file.')
                    return False
        else:
            local_exists = os.path.exists(self._compare_path_or_id)
            local_is_file = local_exists and os.path.isfile(self._compare_path_or_id)

            if not local_exists:
                self._log_error('Local path does not exist: {0}'.format(self._compare_path_or_id))
                return False

            if (start_entity_is_file and local_exists and not local_is_file) or \
                    (not start_entity_is_file and local_exists and local_is_file):
                self._log_error('Starting entity and local path must both be a file.')
                return False

        return True

    def _log_error(self, msg):
        if isinstance(msg, Exception):
            self.result.errors.append(str(msg))
            Logging.exception(msg, console=True)
        else:
            self.result.errors.append(msg)
            Logging.error(msg, console=True)

    async def _worker(self):
        while True:
            args = await self.queue.get()
            if args:
                try:
                    await self._process_children(*args)
                except Exception as ex:
                    self._log_error(ex)
                finally:
                    self.queue.task_done()

    def print_progress(self, msg=None, inc_total=True):
        if inc_total:
            self.total_items_found += 1
        Utils.print_inplace('[Items Found: {0}] {1}'.format(self.total_items_found, msg))

    async def _process_children(self, left_parent, left_local_path, right_parent=None):
        try:
            has_left = left_parent.id is not None
            has_right = right_parent is not None and right_parent.id is not None

            left_remote_synapse_root_path = await self._remote_abs_base_path(left_parent) if has_left else None
            right_remote_synapse_root_path = await self._remote_abs_base_path(right_parent) if has_right else None

            left_items = []
            right_items = []

            if isinstance(left_parent, syn.File):
                # Comparing a single file.
                left_item = SynapseItem(SynapseItem.Types.FILE,
                                        id=left_parent.id,
                                        parent_id=left_parent.parentId,
                                        name=left_parent.name,
                                        synapse_root_path=left_remote_synapse_root_path,
                                        local_root_path=os.path.dirname(left_local_path))
                left_items.append(left_item)

                if right_parent is not None:
                    right_item = SynapseItem(SynapseItem.Types.FILE,
                                             id=right_parent.id,
                                             parent_id=right_parent.parentId,
                                             name=right_parent.name,
                                             synapse_root_path=right_remote_synapse_root_path,
                                             local_root_path=os.path.dirname(
                                                 left_local_path))
                    right_items.append(right_item)
            else:
                # Get left items.
                if has_left:
                    async for child in Synapsis.Chain.getChildren(left_parent, includeTypes=["folder", "file"]):
                        child_id = child.get('id')
                        child_name = child.get('name')
                        is_folder = child.get('type') == 'org.sagebionetworks.repo.model.Folder'
                        child_display_type = 'Folder' if is_folder else 'File'
                        child_type = SynapseItem.Types.FOLDER if is_folder else SynapseItem.Types.FILE

                        left_item = SynapseItem(child_type,
                                                id=child_id,
                                                parent_id=left_parent.id,
                                                name=child_name,
                                                synapse_root_path=left_remote_synapse_root_path,
                                                local_root_path=left_local_path)
                        await left_item.load()
                        left_items.append(left_item)
                        self.print_progress(msg='{0}: {1}'.format(child_display_type, left_item.synapse_path))

                # Get right items.
                if has_right:
                    async for child in Synapsis.Chain.getChildren(right_parent, includeTypes=["folder", "file"]):
                        child_id = child.get('id')
                        child_name = child.get('name')
                        is_folder = child.get('type') == 'org.sagebionetworks.repo.model.Folder'
                        child_display_type = 'Folder' if is_folder else 'File'
                        child_type = SynapseItem.Types.FOLDER if is_folder else SynapseItem.Types.FILE
                        right_item = SynapseItem(child_type,
                                                 id=child_id,
                                                 parent_id=right_parent.id,
                                                 name=child_name,
                                                 synapse_root_path=right_remote_synapse_root_path,
                                                 local_root_path=left_local_path)
                        await right_item.load()
                        right_items.append(right_item)
                        self.print_progress(msg='{0}: {1}'.format(child_display_type, right_item.synapse_path))

            # Match up the items and process folders
            for left_item in left_items:
                if has_right:
                    right_item = self._get_comparable_for(right_parent.synapse_path, right_items, name=left_item.name)
                    if right_item is None:
                        right_item = SynapseItem(left_item.type,
                                                 id=None,
                                                 parent_id=right_parent.id,
                                                 name=left_item.name,
                                                 synapse_root_path=right_remote_synapse_root_path,
                                                 local_root_path=left_local_path)
                    left_item.compare_item = right_item
                    right_item.compare_item = left_item
                self._add_comparable(left_item, self.left_comparables)
                if left_item.is_folder:
                    await self.queue.put([left_item, left_item.local.abs_path, right_item])

            for right_item in right_items:
                if right_item.compare_item is None:
                    left_item = SynapseItem(right_item.type,
                                            id=None,
                                            parent_id=left_parent.id,
                                            name=right_item.name,
                                            synapse_root_path=left_remote_synapse_root_path or left_parent.synapse_path,
                                            local_root_path=left_local_path)
                    left_item.compare_item = right_item
                    right_item.compare_item = left_item
                    self._add_comparable(left_item, self.left_comparables)
                    if right_item.is_folder:
                        await self.queue.put([left_item, left_item.local.abs_path, right_item])

        except Exception as ex:
            self._log_error(ex)

    def can_skip(self, synapse_item):
        skip_values = [
            synapse_item.id,
            synapse_item.name,
            synapse_item.synapse_path,
            synapse_item.local.abs_path,
            synapse_item.local.name
        ]
        for skip_value in skip_values:
            if skip_value in self._excludes:
                return True

        return False

    REMOTE_ABS_BASE_PATH = {}

    async def _remote_abs_base_path(self, parent):
        parent_id = Synapsis.id_of(parent)

        if parent_id not in self.REMOTE_ABS_BASE_PATH:
            if parent_id in self.left_comparables and self.left_comparables[parent_id]:
                path = self.left_comparables[parent_id][0].synapse_root_path
            else:
                path = await Synapsis.Chain.get_synapse_path(parent_id)

            self.REMOTE_ABS_BASE_PATH[parent_id] = path

        return self.REMOTE_ABS_BASE_PATH[parent_id]

    def _get_comparable_for(self, synapse_path, comparables, abs_path=None, name=None):
        if isinstance(comparables, list):
            parent_items = comparables
        else:
            parent_items = comparables.get(synapse_path, [])
        if abs_path:
            return next((c for c in parent_items if c.local.abs_path == abs_path), None)
        elif name:
            return next((c for c in parent_items if c.name == name), None)
        else:
            return parent_items

    def _add_comparable(self, synapse_item, comparables):
        synapse_path = synapse_item.synapse_path
        if synapse_path not in comparables:
            comparables[synapse_path] = []
        if synapse_item not in comparables[synapse_path]:
            comparables[synapse_path].append(synapse_item)
        return synapse_item

    async def _compare_remote(self, left_parent):
        try:
            print_to_console = self.total_items_found <= 1000

            left_comparables = self._get_comparable_for(left_parent.synapse_path, self.left_comparables)
            left_comparables.sort(key=lambda c: c.synapse_path)

            # Remove any ignored files
            if self._excludes:
                for c in left_comparables:
                    if self.can_skip(c):
                        left_comparables.remove(c)
                        if c.exists:
                            Logging.info('[SKIPPING] {0}'.format(c.synapse_path), console=print_to_console)

            # Compare
            for left_comparable in left_comparables:
                right_comparable = left_comparable.compare_item

                if left_comparable.exists and not right_comparable.exists:
                    Logging.warning('[-] {0} -> {1} [{2} NOT FOUND]'.format(
                        left_comparable.synapse_path,
                        right_comparable.synapse_path,
                        left_comparable.type),
                        console=print_to_console)
                    self.result.missing.append(right_comparable)
                elif not left_comparable.exists and right_comparable.exists:
                    Logging.warning('[-] {0} <- {1} [{2} NOT FOUND]'.format(
                        left_comparable.synapse_path,
                        right_comparable.synapse_path,
                        left_comparable.type),
                        console=print_to_console)
                    self.result.missing.append(left_comparable)
                else:
                    if left_comparable.is_folder:
                        Logging.info('[+] {0} <-> {1}'.format(
                            left_comparable.synapse_path,
                            right_comparable.synapse_path),
                            console=print_to_console)
                    else:
                        if left_comparable.content_size is None:
                            Logging.info('[+] {0} <-> {1} [SYNAPSE FILE SIZE/MD5 UNKNOWN]'.format(
                                left_comparable.synapse_path,
                                right_comparable.synapse_path),
                                console=print_to_console)
                        else:
                            left_content_size = left_comparable.content_size
                            right_content_size = right_comparable.content_size
                            if left_content_size != right_content_size:
                                Logging.warning('[-] {0} {1} <- {2} {3} [FILE SIZE MISMATCH]'.format(
                                    left_comparable.synapse_path,
                                    Utils.pretty_size(left_comparable.content_size),
                                    right_comparable.synapse_path,
                                    Utils.pretty_size(right_content_size)),
                                    console=print_to_console)
                                self.result.not_equal.append(right_comparable)
                                self.result.not_equal.append(left_comparable)
                            else:
                                left_md5 = left_comparable.content_md5
                                right_md5 = left_comparable.content_md5
                                if left_md5 != right_md5:
                                    Logging.warning('[-] {0} {1} <- {2} {3} [FILE MD5 MISMATCH]'.format(
                                        left_comparable.synapse_path,
                                        left_md5,
                                        right_comparable.synapse_path,
                                        right_md5),
                                        console=print_to_console)
                                    self.result.not_equal.append(right_comparable)
                                    self.result.not_equal.append(left_comparable)
                                else:
                                    Logging.info('[+] {0} <-> {1}'.format(
                                        left_comparable.synapse_path,
                                        right_comparable.synapse_path),
                                        console=print_to_console)
                    if left_comparable.is_folder:
                        await self._compare_remote(left_comparable)
                self.result.total_compared += 2
        except Exception as ex:
            Logging.exception(ex, console=True)

    async def _compare_local(self, parent, local_path):
        print_to_console = self.total_items_found <= 1000
        try:
            if os.path.isfile(local_path):
                local_items = list(os.scandir(os.path.dirname(local_path)))
                local_items = [f for f in local_items if f.path == local_path]
            else:
                local_items = list(os.scandir(local_path))
            comparables = sorted(self._get_comparable_for(parent.synapse_path, self.left_comparables),
                                 key=lambda c: c.synapse_path)

            # Add missing locals.
            for local in local_items:
                comparable = self._get_comparable_for(parent.synapse_path, comparables, abs_path=local.path)
                if not comparable:
                    remote_abs_base_path = await self._remote_abs_base_path(parent)
                    entity_type = SynapseItem.Types.FOLDER if local.is_dir() else SynapseItem.Types.FILE
                    comparable = SynapseItem(entity_type,
                                             name=local.name,
                                             parent_id=parent,
                                             synapse_root_path=remote_abs_base_path,
                                             local_root_path=local_path)
                    comparables.append(comparable)

            comparables.sort(key=lambda c: c.synapse_path)

            # Remove any ignored files
            if self._excludes:
                for c in comparables:
                    if self.can_skip(c):
                        comparables.remove(c)
                        if c.local.exists:
                            Logging.info('[SKIPPING] {0}'.format(c.local.abs_path), console=print_to_console)
                        if c.exists:
                            Logging.info('[SKIPPING] {0}'.format(c.synapse_path), console=print_to_console)

            # Compare
            for c in comparables:
                if c.is_folder:
                    if c.local.exists and not c.exists:
                        Logging.warning('[-] {0} <- {1} [FOLDER NOT FOUND ON SYNAPSE]'.format(
                            c.synapse_path,
                            c.local.abs_path),
                            console=print_to_console)
                        self.result.missing.append(c)
                    elif c.exists and not c.local.exists:
                        Logging.warning('[-] {0} -> {1} [FOLDER NOT FOUND LOCALLY]'.format(
                            c.synapse_path,
                            c.local.abs_path),
                            console=print_to_console)
                        self.result.missing.append(c)
                    else:
                        Logging.info('[+] {0} <-> {1}'.format(
                            c.synapse_path,
                            c.local.abs_path),
                            console=print_to_console)
                        await self._compare_local(c.id, c.local.abs_path)
                        # await self.queue.put([c.id, c.local.abs_path])
                else:
                    if c.local.exists and not c.exists:
                        Logging.warning('[-] {0} <- {1} [FILE NOT FOUND ON SYNAPSE]'.format(
                            c.synapse_path,
                            c.local.abs_path),
                            console=print_to_console)
                        self.result.missing.append(c)
                    elif c.exists and not c.local.exists:
                        Logging.warning('[-] {0} -> {1} [FILE NOT FOUND LOCALLY]'.format(
                            c.synapse_path,
                            c.local.abs_path),
                            console=print_to_console)
                        self.result.missing.append(c)
                    else:
                        if c.content_size is None:
                            Logging.info('[+] {0} <-> {1} [SYNAPSE FILE SIZE/MD5 UNKNOWN]'.format(
                                c.synapse_path,
                                c.local.abs_path),
                                console=print_to_console)
                        else:
                            local_size = c.local.content_size
                            if local_size != c.content_size:
                                Logging.warning('[-] {0} {1} <- {2} {3} [FILE SIZE MISMATCH]'.format(
                                    c.synapse_path,
                                    Utils.pretty_size(c.content_size),
                                    c.local.abs_path,
                                    Utils.pretty_size(local_size)),
                                    console=print_to_console)
                                self.result.not_equal.append(c)
                            else:
                                local_md5 = c.local.content_md5
                                if local_md5 != c.content_md5:
                                    Logging.warning('[-] {0} {1} <- {2} {3} [FILE MD5 MISMATCH]'.format(
                                        c.synapse_path,
                                        c.content_md5,
                                        c.local.abs_path,
                                        local_md5),
                                        console=print_to_console)
                                    self.result.not_equal.append(c)
                                else:
                                    Logging.info('[+] {0} <-> {1}'.format(c.synapse_path, c.local.abs_path),
                                                 console=print_to_console)
        except Exception as ex:
            Logging.exception(ex, console=True)


class CompareResult:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.total_compared = 0
        self.missing = []
        self.not_equal = []
        self.errors = []
