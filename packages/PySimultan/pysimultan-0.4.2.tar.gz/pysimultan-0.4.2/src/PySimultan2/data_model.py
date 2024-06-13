import atexit
import os
import shutil
from uuid import uuid4
from colorlog import getLogger
from weakref import WeakSet, WeakValueDictionary
from . import config
from .utils import *
from pathlib import PosixPath, WindowsPath
from typing import Union, Tuple, TYPE_CHECKING


# from SIMULTAN import Projects
# noinspection PyUnresolvedReferences
from SIMULTAN.Projects import ExtendedProjectData
# noinspection PyUnresolvedReferences
from SIMULTAN import Utils
# noinspection PyUnresolvedReferences
from SIMULTAN.Data import Users as SimultanUsers
# from SIMULTAN.Serializer import Projects
from SIMULTAN.Serializer.SimGeo import *
from SIMULTAN.Serializer.Projects import *
from SIMULTAN.Data.Components import SimComponent
from SIMULTAN.Data.MultiValues import SimMultiValueBigTable, SimMultiValueField3D
from SIMULTAN.Data.Assets import ResourceEntry
from SIMULTAN.Data.Geometry import OffsetAlgorithm
# from GeometryViewer.Service import *
# from SIMULTAN.UI.Services import *
from System.IO import *
from System.Collections.Generic import *
from System.Collections.Generic import List as NetList
from SIMULTAN.Data.Taxonomy import SimTaxonomyEntry, SimTaxonomyEntryReference, SimTaxonomy
from SIMULTAN.Data.Geometry import GeometryModel as NetGeometryModel
from SIMULTAN.Data.Geometry import Layer, Vertex, Edge, PEdge, Face, Volume, EdgeLoop

from System.Security import SecureString
from System import Guid
from System.IO import *
from System.Security import *
from System.Security.Cryptography import *
from System.Text import *

from .files import add_tag_to_resource


if TYPE_CHECKING:
    from .object_mapper import PythonMapper
    from .geometry import GeometryModel


logger = getLogger('PySimultan')


class IAuthenticationServiceNew(SimultanUsers.IAuthenticationService):
    __namespace__ = "authenticate_namespace"

    user_name = None
    password = None

    def Authenticate(self, user_manager, project_file):
        # user_name = 'admin'
        # password = 'admin'

        sec_str = SecureString()
        for char in self.password:
            sec_str.AppendChar(char)

        user = user_manager.Authenticate(self.user_name, sec_str)

        user_manager.CurrentUser = user.Item1
        user_manager.EncryptionKey = user.Item2

        return user.Item1


data_models = WeakSet()
data_models_dict = WeakValueDictionary()


# noinspection PyUnresolvedReferences
class DataModel:

    @classmethod
    def create_new_project(cls, project_path: str, user_name: str = 'admin', password: str = 'admin'):
        """
        Create a new project
        :param project_path: Project path, e.g. 'C:/Users/username/Documents/Project1.simultan'
        :param user_name:
        :param password:
        :return: DataModel
        """

        passwordArray = Encoding.UTF8.GetBytes(password)
        encryptionKey = RandomNumberGenerator.GetBytes(32)
        encryptedEncryptionKey = SimultanUsers.SimUsersManager.EncryptEncryptionKey(encryptionKey, passwordArray)
        passwordHash = SimultanUsers.SimUsersManager.HashPassword(passwordArray)
        initialUser = SimultanUsers.SimUser(Guid.NewGuid(),
                                            user_name,
                                            passwordHash,
                                            encryptedEncryptionKey,
                                            SimultanUsers.SimUserRole.ADMINISTRATOR)

        tempPath = Path.GetTempPath()
        projectFile = FileInfo(project_path)
        projectData = ExtendedProjectData()

        projectData.UsersManager.EncryptionKey = encryptionKey
        if projectFile.Exists:
            projectFile.Delete()
        project = ZipProjectIO.NewProject(projectFile, tempPath, projectData, initialUser)
        projectFile.Refresh()
        if projectFile.Exists:
            print("Project created successfully")
        else:
            print("Failed to create project")

        return cls(project_path=project_path, user_name=user_name, password=password, project_data_manager=projectData)

    def __new__(cls, *args, **kwargs):

        instance = super().__new__(cls)
        config.set_default_data_model(instance)
        try:
            data_models.add(instance)
        except Exception as e:
            logger.error(f'Error adding instance {instance} to data_models: {e}')
        return instance

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        """
        self.user_name: str = kwargs.get('user_name', 'admin')
        self.password: str = kwargs.get('password', 'admin')

        self.models_dict = {}

        atexit.register(self.cleanup)

        self.id = uuid4()
        data_models_dict[self.id] = self
        self.data = None
        self._project_data_manager = None
        self._user = None
        self._project = None
        self._zip_loader = None

        self.project_data_manager = kwargs.get('project_data_manager', None)

        self.project_path = kwargs.get('project_path', None)

        self.service_provider = Utils.ServicesProvider()

        self.i_aut_service = IAuthenticationServiceNew
        self.i_aut_service.user_name = self.user_name
        self.i_aut_service.password = self.password

        self.service_provider.AddService[SimultanUsers.IAuthenticationService](self.i_aut_service())
        self.exch = self.project.AllProjectDataManagers.ComponentGeometryExchange
        # self.exch.ModelStore = self.serv

        self.resources = {}
        self.import_data_model()

        self.__mongo_instance = None

    @property
    def assets(self):
        return self.project_data_manager.AssetManager.Resources

    @property
    def models(self) -> dict[int, 'GeometryModel']:
        """
        Return the geometry models of the project
        :return: dict[int, GeometryModel]
        """

        # if self.models_dict:
        #     return self.models_dict

        self.models_dict = {}

        # self.project_data_manager.Reset()

        resources = self.project_data_manager.AssetManager.Resources

        for resource in resources:
            if resource is None:
                continue
            self.resources[resource.Key] = resource

            current_full_path = resource.CurrentFullPath
            if current_full_path == '?':
                continue

            if resource.Extension == '.simgeo':
                self.models_dict[resource.Key] = None
                error_list = NetList[SimGeoIOError]()

                model = SimGeoIO.Load(resource, self.project_data_manager, error_list, OffsetAlgorithm.Full)
                self.models_dict[resource.Key] = model
                try:
                    self.project_data_manager.GeometryModels.AddGeometryModel(model)
                except Exception as e:
                    logger.warning(f'Error while loading Model: {model} from {model.File}: {e}')
                    raise e

        return self.models_dict

    @property
    def taxonomies(self):
        return self.project_data_manager.Taxonomies

    @property
    def ValueFields(self):
        return self.project_data_manager.ValueManager.Items

    @property
    def value_fields(self):
        return self.project_data_manager.ValueManager

    @property
    def project_data_manager(self):

        if self._project_data_manager is None:
            self._project_data_manager = ExtendedProjectData()

        return self._project_data_manager

    @project_data_manager.setter
    def project_data_manager(self, value):
        self._project_data_manager = value

    @property
    def user(self) -> SimultanUsers.SimUserRole:
        if self._user is None:
            self._user = SimultanUsers.SimUserRole.ADMINISTRATOR
        return self._user

    @user.setter
    def user(self, value: SimultanUsers.SimUserRole):
        if value != self._user:
            self._project = None
        self._user = value

    @property
    def project(self):
        if (self._project is None) and (self.project_path is not None) and (self.project_data_manager is not None):
            logger.debug('loading project')
            self.project = ZipProjectIO.Load(FileInfo(self.project_path), self.project_data_manager)
            exit_code = ZipProjectIO.AuthenticateUserAfterLoading(self.project,
                                                                  self.project_data_manager,
                                                                  self.service_provider)
            if not exit_code:
                logger.error('Could not open project. Wrong user or password! Exiting program...')
            ZipProjectIO.OpenAfterAuthentication(self.project, self.project_data_manager)
            logger.debug('project loaded successfull')
        return self._project

    @project.setter
    def project(self, value):
        self._project = value

    def get_typed_data(self, mapper: 'PythonMapper', create_all=False) -> list[SimultanObject]:
        """
        Return the typed data from the project
        :param mapper:
        :param create_all: If True, all components and subcomponents will be created, else only the top level components
        :return:
        """

        mapper._create_all = create_all
        mapper.current_data_model = self

        return mapper.get_typed_data(self, create_all=create_all)

    def import_data_model(self):
        self.data = self.project_data_manager.Components
        return self.data

    def add_field(self, field: SimMultiValueField3D):
        self.project_data_manager.ValueManager.Add(field)

    def remove_field(self, field: SimMultiValueField3D):
        self.project_data_manager.ValueManager.Remove(field)

    def get_geo_instance(self, file_id, type, id):
        geo_model = self.models[file_id]
        objects = getattr(geo_model.Geometry, type)

        return next((x for x in objects.Items if x.Id == id), None)

    def add_component(self, component: SimComponent):
        """
        Add a component to the project
        :param component:
        :return:
        """
        # logger.info(
        #     f'Adding component {component.Id} {component.Name} {type(component)} to project {self.project_path}')
        if component.Id.LocalId != 0:
            raise ValueError(f'Component {component.Id} already added to project {self.project_path}')

        if not hasattr(component, '__added_to_data_model__'):
            component.__added_to_data_model__ = True
        elif component.__added_to_data_model__:
            return

        self.data.Add(component)
        # logger.info(
        #     f'Added component {component.Id} {component.Name} {type(component)} to project {self.project_path}')

    def create_new_component(self,
                             name: str,
                             slot: Union[None, SimTaxonomyEntry, SimTaxonomyEntryReference] = None,
                             add_to_project=True,
                             **kwargs) -> SimultanObject:
        """
        Create a new component and add it to the project
        :param name: Name of the component
        :param slot: Slot of the component
        :param add_to_project: Add the component to the project
        :param kwargs:
        :return: SimultanObject
        """

        comp = create_component(name=name,
                                slot=slot,
                                data_model=self,
                                **kwargs)
        if add_to_project:
            self.add_component(comp)
        return comp

    def remove_subcomponent(self, component: SimComponent = None, index: int = None):
        """
        Remove a subcomponent from a component
        :param component:
        :param index:
        :return:
        """
        if component is not None:
            index = self.data.Items.IndexOf(component)
            self.data.RemoveItem(index)
        elif index is not None:
            self.data.RemoveItem(index)

    def save(self):
        """
        Save the project
        :return:
        """
        ZipProjectIO.Save(self.project, False)

    def cleanup(self):
        """
        Close and cleanup project
        """
        logger.info('closing project...')
        try:

            self._project.DisableProjectUnpackFolderWatcher()
            if self._project is not None:
                if self._project.IsOpened:
                    ZipProjectIO.Close(self._project, True)
                if self._project.IsLoaded:
                    ZipProjectIO.Unload(self._project)

        except Exception as e:
            pass
        finally:
            if self._project_data_manager is not None:
                del self._project_data_manager
            self._project_data_manager = None

            data_models = WeakSet()
            data_models_dict = WeakValueDictionary()

            if config.get_default_data_model() is self:
                config.set_default_data_model(None)

            del self

    # def create_new_component(self):
    #
    #     ref_comp = self.data.Items[0]
    #
    #     new_comp = SimComponent()
    #     new_comp.Name = 'Test'
    #
    #     new_param = SimParameter('test_param', 'Unicorn', 15.268)
    #     new_comp.Parameters.Add(new_param)
    #
    #     sub_new_comp = SimComponent()
    #     sub_new_comp.CurrentSlot = SimSlotBase(ComponentUtils.COMP_SLOT_AREAS)
    #     sub_new_comp.Name = 'SubTest'
    #
    #     entry = SimChildComponentEntry(SimSlot(SimSlotBase(ComponentUtils.COMP_SLOT_AREAS), '15'),
    #                                    sub_new_comp)
    #     new_comp.Components.Add(entry)
    #
    #     slot = SimSlot(ref_comp.CurrentSlot, '11')
    #     ComponentManagement.AddReferencedComponentSlot(new_comp, slot, self.user)
    #     ComponentManagement.AddReferencedComponent(new_comp, slot, ref_comp, self.user)
    #
    #     self.add_component(new_comp)
    #     self.save()
    #
    #     return new_comp

    def add_component_reference(self, comp: SimComponent, ref_comp: SimComponent, slot_extension: str, slot_name: str):
        """
        Add a reference to a component
        :param comp: Component to add the reference
        :param ref_comp: Referenced component
        :param slot_extension:
        :param slot_name:
        :return:
        """
        slot = SimSlot(slot_name, str(slot_extension))
        ComponentManagement.AddReferencedComponentSlot(comp, slot, self.user)
        ComponentManagement.AddReferencedComponent(comp, slot, ref_comp, self.user)

    def remove_referenced_component(self, comp: SimComponent, index: int):
        if index is not None:
            self.data.RemoveItem(index)
        elif comp is not None:
            index = self.data.Items.IndexOf(comp)
            self.data.RemoveItem(index)

    def add_new_geometry_model(self, file_name: str, model_name: str = None, return_resource=False):
        """
        Create and add a new geometry model
        :param file_name: name of the created .simgeo file
        :param model_name: name of the geometry model
        :param return_resource: return the resource
        :return: GeometryViewer.Model.GeometryModel, geo_resource
        """
        geo_resource = self.add_geometry_resource(file_name)
        file_info = FileInfo(geo_resource.CurrentFullPath)
        try:
            model = SimGeoIO.Load(file_info, self.inst, self.serv)
            self.models_dict[geo_resource.Key] = model
            self.serv.AddGeometryModel(model)
        except ArgumentOutOfRangeException as e:
            logger.warning(f'Error while loading Model: {model} from {model.File}: {e}. Trying reload...')
            model = SimGeoIO.Load(file_info, self.inst, self.serv)
            self.models_dict[geo_resource.Key] = model
            self.serv.AddGeometryModel(model)

        if model_name is not None:
            model.Name = model_name

        if return_resource:
            return model, geo_resource
        else:
            return model

    def add_geometry_resource(self, model_name: str):
        """
        Add / create new geometry resource (.simgeo file)
        :param model_name: name of the new .simgeo file without file extension; Example: 'new_model'
        """
        self.service_provider.GetService[IGeometryViewerService]()
        new_resource = self.project.AddEmptyGeometryResource(self.project.ProjectUnpackFolder,
                                                             model_name,
                                                             self.service_provider)

        return new_resource

    def add_empty_resource(self, filename: str):
        """
        Add an empty resource to the project
        :param file_name: name of the new resource
        :return:
        """
        # return self.project.AddResourceFile(FileInfo(str(filename)))

        return self.project.AddEmptyResource(FileInfo(str(filename)))

    def add_resource(self,
                     filename: Union[str, FileInfo],
                     tag: Union[SimTaxonomyEntry, SimTaxonomyEntryReference] = None) -> ResourceEntry:
        """
        Add a new resource to the project. The resource will be copied to the project folder and added to the project
        :param filename: path to the file or FileInfo object
        :param tag: tag to add to the resource
        :return:
        """

        del_copy = False

        existing_files = [x.Name for x in self.project_data_manager.AssetManager.Resources]
        try:
            act_filename = filename.replace('\\', os.sep)
        except TypeError:
            act_filename = filename

        if os.path.basename(act_filename) in existing_files:
            # create copy with running counter in temp dir and use this file:
            counter = 1
            while True:
                new_filename = os.path.basename(filename) + f'({str(counter)})'
                if new_filename not in existing_files and not os.path.exists(new_filename):
                    break
                counter += 1
            shutil.copy(filename, os.path.join(os.path.dirname(filename),  new_filename))
            filename = os.path.join(os.path.dirname(filename),  new_filename)
            del_copy = True

        if isinstance(filename, (str, PosixPath, WindowsPath)):
            filename = FileInfo(str(filename))

        resource = self.project.CopyResourceAsContainedFileEntry(filename,
                                                                 self.project.ProjectUnpackFolder,
                                                                 '1')

        if del_copy:
            os.remove(str(filename))

        # file_id = self.project_data_manager.AssetManager.AddResourceEntry(FileInfo(filename))
        # return self.project_data_manager.AssetManager.Resources[file_id]
        if tag is not None:
            add_tag_to_resource(resource, tag)

        return resource

    def delete_resource(self, resource: Union[ResourceEntry, FileInfo, ContainedResourceFileEntry]):
        """
        Delete a resource from the project and the project folder
        :param resource: resource to delete
        :return:
        """

        if isinstance(resource, FileInfo):
            resource = resource.resource_entry

        success = self.project.DeleteResource(resource)
        if success:
            logger.info(f'Deleted resource {resource.Name} from project {self.project_path}')
        else:
            logger.error(f'Could not delete resource {resource.Name} from project {self.project_path}')
        return success

    def add_table(self, table: SimMultiValueBigTable):
        self.project_data_manager.ValueManager.Add(table)

    def find_components_with_taxonomy(self, taxonomy: str, component_list=None, first=False):

        if component_list is None:
            component_list = self.data.Items

        return find_components_with_taxonomy(component_list, taxonomy, first)

    def get_associated_geometry(self, component: Union[SimComponent, SimultanObject]) -> list[Tuple[Union[Layer, Vertex, Edge, PEdge, Face, Volume, EdgeLoop], NetGeometryModel]]:

        ref_geometries = []

        if isinstance(component, SimultanObject):
            component = component._wrapped_obj

        for instance in component.Instances:
            for placement in instance.Placements.Items:
                geo_model = next((x for x in self.models.values() if x is not None and x.File.Key == placement.FileId), None)
                if geo_model is not None:
                    ref_geometries.append((geo_model.Geometry.GeometryFromId(placement.GeometryId), geo_model))
                if geo_model is None:
                    logger.warning(f'Geometry model with id {placement.FileId} not found in project {self.project_path}')

        return ref_geometries

    def get_referenced_components(self, geometry):
        return list(self.exch.GetComponents(geometry))

        # if geometry_model is None:
        #     geos = {}
        #     for geometry_model in self.models:
        #         geo = get_component_geometry(self, geometry_model, component)
        #         geos[geometry_model] = geo
        #     return geos
        # else:
        #     return get_component_geometry(self, geometry_model, component)

    def create_taxonomy(self, name: str, key: str, description: str = ''):
        """
        Create a new taxonomy and add it to the project
        :param name:
        :param key:
        :param description:
        :return:
        """
        return create_taxonomy(name, key, description, data_model=self)

    def get_taxonomy_entry(self, key):
        for entry in self.taxonomies:
            if entry.Key == key:
                return entry

    def create_mongo_instance(self):
        from .mongo_utils.base_classes import DataModel as MongoDataModel
        from .redis_utils.base_classes import save_in_redis

        logger.info(f'Creating mongo instance for project {self.project_data_manager.Project.Name}')
        self._mongo_instance, created = MongoDataModel.get_or_create(self)
        if created:
            logger.info(f'Created new mongo instance for {self.project_data_manager.Project.Name}')
        else:
            logger.info(f'Found existing mongo instance for {self.project_data_manager.Project.Name}')

    def save_in_mongodb(self, db):
        """
        save the object in the mongodb database
        :param db: mongodb database
        :return: None
        """
        self._mongo_instance.save(db)

    def save_in_redis(self):
        """
        save the object in the redis database
        :return: None
        """
        save_in_redis(self)

    def get_taxonomy_entries(self):

        def add_sub_entries(tax_entry, tax_entries_dict):
            for sub_entry in tax_entry.Children:
                tax_entries_dict[sub_entry.Key] = sub_entry
                tax_entries_dict = add_sub_entries(sub_entry, taxonomy_entries)
            return tax_entries_dict

        taxonomy_entries = {}
        for taxonomy in self.taxonomies:
            taxonomy_entries[taxonomy.Key] = taxonomy
            for entry in list(taxonomy.Entries):
                taxonomy_entries[entry.Key] = entry
                for child in entry.Children:
                    taxonomy_entries[child.Key] = child
                    taxonomy_entries = add_sub_entries(child, taxonomy_entries)

        return taxonomy_entries

    def create_new_geometry_model(self,
                                  name: str) -> Tuple[NetGeometryModel, ResourceFileEntry]:
        resource_file = self.project.AddEmptyGeometryResource(self._project.ProjectUnpackFolder,
                                                              name,
                                                              f'{0} ({1})',
                                                              self.project.AllProjectDataManagers.DispatcherTimerFactory)
        # Load the geometry model
        model_to_work_with = SimGeoIO.Load(resource_file,
                                           self.project_data_manager,
                                           None)
        return model_to_work_with, resource_file

    def get_or_create_taxonomy(self, taxonomy_key: str, taxonomy_name: str = None, description='', create=True):
        taxonomy = next((x for x in self.taxonomies if x.Key == taxonomy_key), None)
        if taxonomy is None:
            if create:
                self.create_taxonomy(key=taxonomy_key, name=taxonomy_name, description=description)
            else:
                raise ValueError(f'Taxonomy {taxonomy_key} not found in project {self.project_path}')

        return next((x for x in self.taxonomies if x.Key == taxonomy_key), None)

    def get_or_create_taxonomy_entry(self,
                                     name: str,
                                     key: str,
                                     description: str = '',
                                     sim_taxonomy: SimTaxonomy = None) -> SimTaxonomyEntry:
        return get_or_create_taxonomy_entry(name, key, description, sim_taxonomy, data_model=self, create=True)

    def __del__(self):
        self.cleanup()


# if __name__ == '__main__':
#
#     # create example templates
#     templates = create_example_template_bim_bestand_network()
#
#     # write the example templates to a file:
#     with open('example_templates.yml', mode='w') as f_obj:
#         yaml.dump(templates, f_obj)
#
#     # load the example templates:
#     templates = load_templates('example_templates.yml')
#
#     # create classes from the templates:
#     template_classes = create_template_classes(templates)
#
#     simultan_components = create_example_simultan_components(templates, n=5)
#
#     simultan_components = class_type_simultan_components(simultan_components, template_classes)
#
#     # the simultan components are now of the type which is defined in the templates
#     print(simultan_components)
#
#     # the class typed components still keep all methods and attributes from simultan:
#     print(simultan_components[0].simultan_method())
#
#     # and the class typed components have the new defined method python_spec_func:
#     simultan_components[10].python_spec_func()
