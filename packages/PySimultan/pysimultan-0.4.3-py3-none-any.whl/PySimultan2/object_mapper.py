from collections import UserList
from weakref import WeakSet
from typing import Type
from colorlog import getLogger

from . import config
from .data_model import data_models
from .utils import *
from .default_types import ComponentList, component_list_map, ComponentDictionary, component_dict_map

from .simultan_object import SimultanObject
from .geometry.utils import create_python_geometry

from SIMULTAN.Data.Geometry import (Layer, Vertex, Edge, PEdge, Face, Volume, EdgeLoop)
from SIMULTAN.Data.Components import SimComponent
from .geometry.geometry_base import (SimultanLayer, SimultanVertex, SimultanEdge, SimultanEdgeLoop, SimultanFace,
                                     SimultanVolume)

logger = getLogger('PySimultan')

default_registered_classes = {'ComponentList': ComponentList,
                              'ComponentDict': ComponentDictionary}
default_mapped_classes = {}
default_taxonomy_maps = {'ComponentList': component_list_map,
                         'ComponentDict': component_dict_map}


class PythonMapper(object):

    def __new__(cls, *args, **kwargs):
        instance = super(PythonMapper, cls).__new__(cls)
        config.set_default_mapper(instance)
        return instance

    def __init__(self, *args, **kwargs):

        self.name = kwargs.get('name', 'PythonMapper')
        self.registered_classes = default_registered_classes   # dict with all registered classes: {taxonomy: class}
        self.mapped_classes = default_mapped_classes           # dict with all mapped classes: {taxonomy: class}
        self.taxonomy_maps = default_taxonomy_maps             # dict with all taxonomie maps: {taxonomy: taxonomie_map}

        self.registered_geometry_classes = {Layer: SimultanLayer,
                                            Vertex: SimultanVertex,
                                            Edge: SimultanEdge,
                                            Face: SimultanFace,
                                            Volume: SimultanVolume,
                                            EdgeLoop: SimultanEdgeLoop}

        self.re_register = False

    def register(self, taxonomy, cls, taxonomy_map=None):
        if not self.re_register and taxonomy in self.registered_classes.keys():
            return

        self.registered_classes[taxonomy] = cls
        self.taxonomy_maps[taxonomy] = taxonomy_map

    def create_mapped_class(self, taxonomy, cls):

        if any([issubclass(cls, x) for x in (SimultanObject, UserList)]):
            bases = (cls,)
        else:
            bases = (SimultanObject,) + (cls,)

        def new_init(self, *args, **kwargs):
            for base in self.__class__.__bases__:
                base.__init__(self, *args, **kwargs)

        new_class_dict = {'__init__': new_init,
                          '__name__': cls.__name__,
                          '_taxonomy': taxonomy,
                          '_cls_instances': WeakSet(),
                          '_taxonomy_map': self.taxonomy_maps.get(taxonomy, None),
                          '_base': bases,
                          '_object_mapper': self}

        new_class_dict.update(self.get_properties(taxonomy))
        new_class = type(cls.__name__, bases, new_class_dict)

        self.mapped_classes[taxonomy] = new_class

        return new_class

    def get_mapped_class(self, taxonomy) -> Type[SimultanObject]:
        if self.mapped_classes.get(taxonomy, None) is None:
            self.create_mapped_class(taxonomy, self.registered_classes[taxonomy])

        return self.mapped_classes.get(taxonomy, None)

    def get_typed_data(self, data_model=None, component_list=None, create_all=False):

        typed_data = []

        if component_list is None:
            component_list = list(data_model.data.Items)

        if data_model is None:
            data_model = list(data_models)[0]

        if create_all:
            new_component_list = set()

            def get_subcomponents(sim_component: Union[SimComponent, SimultanObject]):
                new_subcomponents = set()
                if isinstance(sim_component, SimultanObject):
                    sim_component = sim_component._wrapped_obj

                if sim_component in new_component_list:
                    return
                else:
                    new_component_list.add(sim_component)

                if sim_component is None:
                    return []

                for sub_component in sim_component.Components.Items:
                    if sub_component is None:
                        continue
                    new_subcomponents.add(sub_component.Component)
                for ref_component in sim_component.ReferencedComponents.Items:
                    if ref_component is None:
                        continue
                    new_subcomponents.add(ref_component.Target)

                for new_subcomponent in new_subcomponents:
                    get_subcomponents(new_subcomponent)

                new_component_list.update(new_subcomponents)

            for component in component_list:
                if component is None:
                    continue
                get_subcomponents(component)
            component_list = list(new_component_list)

        for component in component_list:
            typed_object = self.create_python_object(component, data_model=data_model)
            typed_data.append(typed_object)
        return typed_data

    def create_python_geometry_object(self, component, data_model=None, *args, **kwargs):

        if component is None:
            return None

        if data_model is None:
            logger.warning(f'No data model provided. Using default data model: {config.get_default_data_model().id}.')
            data_model = config.get_default_data_model()

        if isinstance(component, (Layer, Vertex, Edge, PEdge, Face, Volume, EdgeLoop)):
            if isinstance(component, Layer):
                geometry_model = component.Model.Model
            else:
                geometry_model = component.Layer.Model.Model
            cls = self.registered_geometry_classes[type(component)]
            return create_python_geometry(cls, component, data_model, self, geometry_model)
        else:
            self.create_python_object(component, data_model, *args, **kwargs)

    # @lru_cache(maxsize=500)
    def create_python_object(self, component, cls=None, data_model=None, *args, **kwargs):

        if component is None:
            return None

        if data_model is None:
            logger.warning(f'No data model provided. Using default data model: {config.get_default_data_model().id}.')
            data_model = config.get_default_data_model()

        if isinstance(component, (Layer, Vertex, Edge, PEdge, Face, Volume, EdgeLoop)):
            self.create_python_geometry_object(component, data_model, *args, **kwargs)

        if cls is None:
            c_slots = [x.Target.Key for x in component.Slots.Items]
            c_slot = list(set(c_slots) & set(self.registered_classes.keys()))
            if len(c_slot) == 0:
                if c_slots[0] not in self.registered_classes.keys():
                    self.register(c_slots[0], SimultanObject)
                    c_slot = [c_slots[0]]
            elif len(c_slot) > 1:
                num_superclasses = [len(self.registered_classes[x].__mro__) for x in c_slot]
                c_slot = [c_slot[num_superclasses.index(max(num_superclasses))]]
                # raise Warning(f'Component {component} has more than one registered taxonomy: {c_slot}')

            if c_slot[0] not in self.mapped_classes.keys():
                self.create_mapped_class(c_slot[0], self.registered_classes[c_slot[0]])

            cls = self.mapped_classes[c_slot[0]]

        if component is not None and component.Id in cls._cls_instances_dict.keys():
            return cls._cls_instances_dict[component.Id]
        else:
            return create_python_object(component,
                                        cls,
                                        object_mapper=self,
                                        data_model=data_model,
                                        *args,
                                        **kwargs)

    def get_typed_data_with_taxonomy(self, taxonomy: str, data_model=None, first=False):

        tax_components = data_model.find_components_with_taxonomy(taxonomy=taxonomy, first=first)
        return self.get_typed_data(component_list=tax_components)

    def get_properties(self, taxonomy):

        prop_dict = {}
        taxonomy_map = self.taxonomy_maps.get(taxonomy, None)

        if taxonomy_map is None:
            return prop_dict

        for prop in taxonomy_map.content:

            prop_dict[prop.property_name] = add_properties(prop_name=prop.property_name,
                                                           text_or_key=prop.text_or_key,
                                                           content=prop,
                                                           taxonomy_map=taxonomy_map,
                                                           taxonomy=taxonomy)

        return prop_dict

    def clear(self):
        for cls in self.registered_classes.values():
            cls._cls_instances = WeakSet()

        for cls in self.mapped_classes.values():
            cls._cls_instances = WeakSet()
            cls.__property_cache__ = {}

        if config.get_default_mapper() is self:
            config.set_default_mapper(None)

    def copy(self):
        new_mapper = PythonMapper()
        new_mapper.registered_classes = self.registered_classes
        new_mapper.taxonomy_maps = self.taxonomy_maps
        new_mapper.registered_geometry_classes = self.registered_geometry_classes
        return new_mapper


if config.get_default_mapper() is None:
    config.set_default_mapper(PythonMapper())
