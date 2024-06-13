from synapsis import Synapsis


class EntityBundleWrapper:
    def __init__(self, bundle=None):
        self.bundle = bundle or {}
        self._concrete_type = None
        self._synapse_path = None
        self._file_handle = None

    @classmethod
    async def fetch(cls, synapse_id, **kwargs):
        bundle = await Synapsis.Chain.Utils.get_bundle(synapse_id, **kwargs)
        return cls(bundle=bundle)

    @property
    def entity_type(self):
        return self.bundle.get('entityType')

    @property
    def concrete_type(self):
        if self._concrete_type is None:
            self._concrete_type = Synapsis.ConcreteTypes.get(self.bundle or {})

        return self._concrete_type

    @property
    def is_project(self):
        return self.concrete_type.is_project

    @property
    def is_folder(self):
        return self.concrete_type.is_folder

    @property
    def is_file(self):
        return self.concrete_type.is_file

    def is_a(self, *concrete_types):
        return self.concrete_type.is_a(*concrete_types)

    @property
    def entity(self):
        return self.bundle.get('entity')

    @property
    def id(self):
        return self.entity.get('id')

    @property
    def name(self):
        return self.entity.get('name')

    @property
    def has_children(self):
        return self.bundle.get('hasChildren', False)

    @property
    def data_file_handle_id(self):
        return self.entity.get('dataFileHandleId', None)

    @property
    def synapse_path(self):
        if self._synapse_path is None:
            if self.bundle and 'path' in self.bundle:
                paths = self.bundle.get('path').get('path')[1:]
                segments = []
                for path in paths:
                    segments.append(path['name'])
                self._synapse_path = '/'.join(segments)

        return self._synapse_path

    @property
    def file_handle(self):
        if self.is_file and self._file_handle is None:
            if self.bundle.get('fileHandles', None) and self.data_file_handle_id:
                self._file_handle = Synapsis.Utils.find_data_file_handle(self.bundle,
                                                                         data_file_handle_id=self.data_file_handle_id)

            if self._file_handle is None:
                self._file_handle = Synapsis.Utils.get_filehandle(self.id)
        return self._file_handle

    @property
    def file_handle_concrete_type(self):
        return Synapsis.ConcreteTypes.get(self.file_handle)

    @property
    def filename(self):
        file_handle = self.file_handle
        return file_handle.get('fileName', None) if file_handle else None

    @property
    def content_md5(self):
        file_handle = self.file_handle
        return file_handle.get('contentMd5', None) if file_handle else None

    @property
    def content_size(self):
        file_handle = self.file_handle
        return file_handle.get('contentSize', None) if file_handle else None
