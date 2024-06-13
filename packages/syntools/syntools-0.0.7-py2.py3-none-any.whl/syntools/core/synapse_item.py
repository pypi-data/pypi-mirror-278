import os
from synapsis import Synapsis
from .utils import Utils
import synapseclient as syn


class SynapseItem:

    def __init__(self,
                 type,
                 id=None,
                 parent_id=None,
                 name=None,
                 local_root_path=None,
                 synapse_root_path=None,
                 compare_item=None):
        file_handle_id = None
        file_handle = None
        if isinstance(type, syn.Entity) or isinstance(type, dict):
            entity = type
            id = Synapsis.id_of(entity)
            parent_id = entity.get('parentId', None)
            name = entity.get('name', None)
            type = Synapsis.ConcreteTypes.get(entity)
            if type.is_file:
                file_handle_id = entity.get('dataFileHandleId', None)
                file_handle = entity.get('_file_handle', None)

        self.type = type
        self.id = id
        self.parent_id = parent_id
        self.name = name
        self.local_root_path = local_root_path
        self.synapse_root_path = synapse_root_path
        self.file_handle_id = file_handle_id
        self.filename = None
        self.content_size = None
        self.content_md5 = None

        self.local = self.Local(self)
        self.compare_item = compare_item
        if file_handle is not None:
            self.set_file_handle(file_handle)

    @property
    def exists(self):
        return self.id is not None

    @property
    def is_project(self):
        return self.type.is_project

    @property
    def is_folder(self):
        return self.type.is_folder

    @property
    def is_file(self):
        return self.type.is_file

    @property
    def synapse_path(self):
        name = self.name
        if self.is_file and self.filename:
            name = self.filename

        segments = [s for s in [self.synapse_root_path, name] if s]
        return '/'.join(segments)

    @property
    def is_loaded(self):
        if self.is_file and (self.file_handle_id is None or self.filename is None):
            return False

        return True

    async def load(self):
        if not self.is_loaded and self.id is not None:
            if self.is_file:
                filehandle = await Synapsis.Chain.Utils.get_filehandle(self.id)
                self.set_file_handle(filehandle)

        return self

    def set_file_handle(self, file_handle):
        if not self.is_file:
            raise ValueError('File Handle can only be set on files.')
        filehandle = file_handle.get('fileHandle', None) or file_handle
        self.file_handle_id = filehandle.get('id')
        self.filename = filehandle.get('fileName')
        self.content_md5 = filehandle.get('contentMd5')
        self.content_size = filehandle.get('contentSize')

    class Local:
        def __init__(self, synapse_item):
            self.synapse_item = synapse_item

        @property
        def exists(self):
            if self.synapse_item.is_folder or self.synapse_item.is_project:
                return os.path.isdir(self.abs_path)
            else:
                return os.path.isfile(self.abs_path)

        @property
        def abs_path(self):
            name = self.synapse_item.name

            if self.synapse_item.is_file and self.synapse_item.filename is not None:
                name = self.synapse_item.filename

            if name is not None:
                return os.path.abspath(os.path.join(self.synapse_item.local_root_path, name))

            return None

        @property
        def name(self):
            return os.path.basename(self.abs_path)

        @property
        def content_size(self):
            if self.exists:
                return os.path.getsize(self.abs_path)
            return None

        @property
        def content_md5(self):
            if self.exists:
                return Utils.get_md5(self.abs_path)
            return None
