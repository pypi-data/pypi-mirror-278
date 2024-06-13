import os
from ...core import Utils
from synapsis import Synapsis


class FindId:
    def __init__(self, path):
        self._path = path

    async def execute(self):
        result = FindIdResult(self._path)
        try:
            path_parts = list(filter(str.strip, result.norm_path.split(os.sep)))

            if len(path_parts) > 0:
                project_name = path_parts[0]
                project = await Synapsis.Chain.Utils.find_entity(project_name)

                if not project:
                    result.error = 'Cannot find Synapse project with name: {0}'.format(project_name)
                else:
                    result.parts.append(project)

                    if len(path_parts) == 1:
                        result.entity = project
                    else:
                        parent = project
                        last_entity = None
                        for path_part in path_parts[1:]:
                            child = await Synapsis.Chain.Utils.find_entity(path_part, parent=parent)
                            if child:
                                last_entity = child
                                parent = last_entity
                                result.parts.append(last_entity)
                            else:
                                last_entity = None
                                result.error = 'Could not find Synapse entity: {0} in {1} ({2})'.format(path_part,
                                                                                                        parent.name,
                                                                                                        parent.id)
                        if last_entity:
                            result.entity = last_entity
            else:
                result.error = 'Invalid path: {0}'.format(result.norm_path)

            if result.error:
                print('ERROR: {0}'.format(result.error))
                if result.parts:
                    print('Paths Found:')
                    indent = ''
                    for entity in result.parts:
                        indent += ' '
                        print('{0}{1} ({2})'.format(indent, entity.name, entity.id))
            elif result.id:
                print(result.id)
        except Exception as ex:
            result.error = str(ex)

        return result


class FindIdResult:
    def __init__(self, path):
        self.path = path
        self.norm_path = Utils.norm_os_path_sep(self.path)
        self.error = None
        self.parts = []
        self.entity = None

    @property
    def id(self):
        if self.entity:
            return self.entity.id
        else:
            return None
