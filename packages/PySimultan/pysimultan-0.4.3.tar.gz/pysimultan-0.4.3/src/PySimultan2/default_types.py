from __future__ import annotations

import xxsubtype
from collections.abc import Iterable
import numpy as np
import pandas as pd
import colorlog
from typing import Union, List, Type, Set, Tuple, Any, Optional

from .utils import (sort_slots, create_simultan_component_for_taxonomy, create_mapped_python_object,
                    set_property_to_sim_component, set_property_to_parameter, set_property_to_file_info,
                    set_property_to_list, set_property_to_value_field, set_property_to_unknown_type,
                    remove_prop_from_sim_component, get_param_indices, set_property_to_dict, get_obj_value,
                    get_component_taxonomy_entry)
from .simultan_object import SimultanObject
from .taxonomy_maps import TaxonomyMap, Content

from SIMULTAN.Data.Components import (ComponentWalker, SimComponent, SimBoolParameter, SimDoubleParameter,
                                      SimEnumParameter, SimIntegerParameter, SimStringParameter, ComponentMapping,
                                      SimSlot, SimComponentVisibility, SimChildComponentEntry, SimDefaultSlots,
                                      SimParameterOperations, SimComponentReference)
from .files import FileInfo

from . import config

logger = colorlog.getLogger('PySimultan')


class ComponentList(SimultanObject):

    _create_all = False     # if true all properties are evaluated to create python objects when initialized
    _taxonomy = 'ComponentList'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component_policy = kwargs.get('component_policy', 'subcomponent')  # component add policy of the content/parameter/property, 'reference' or 'subcomponent'
        self.index = 0

    @classmethod
    def create_from_values(cls,
                           values: Union[List[SimultanObject], Set[SimultanObject], Tuple[SimultanObject]],
                           data_model=None,
                           object_mapper=None,
                           *args,
                           **kwargs,
                           ):

        # logger.debug(f'Creating new component list from values {values}')

        wrapped_obj = create_simultan_component_for_taxonomy(cls,
                                                             data_model=data_model,
                                                             object_mapper=object_mapper,
                                                             add_to_data_model=kwargs.get('add_to_data_model', True))

        new_component_list = cls(wrapped_obj=wrapped_obj,
                                 data_model_id=data_model.id,
                                 object_mapper=object_mapper,
                                 data_model=data_model,
                                 )

        wrapped_obj.Name = kwargs.get('name', 'UnnamedComponentList')

        new_component_list.append(values)

        # for i, value in enumerate(values):
        #     if isinstance(value, SimultanObject):
        #         try:
        #             new_component_list.add_referenced_component(value._wrapped_obj,
        #                                                         slot_extension=str(i),
        #                                                         slot=value.slot)
        #         except Exception as e:
        #             logger.error(f'Could not add component {value} to list {new_component_list}:\n{e}')
        #     else:
        #         new_val = create_mapped_python_object(value,
        #                                               data_model=data_model,
        #                                               object_mapper=object_mapper,
        #                                               add_to_data_model=True)
        #
        #         taxonomy = data_model.get_or_create_taxonomy(taxonomy_name=new_val._taxonomy_map.taxonomy_name,
        #                                                      taxonomy_key=new_val._taxonomy_map.taxonomy_key)
        #
        #         taxonomy_entry = data_model.get_or_create_taxonomy_entry(name=new_val._taxonomy_map.taxonomy_entry_name,
        #                                                                  key=new_val._taxonomy_map.taxonomy_entry_key,
        #                                                                  sim_taxonomy=taxonomy)
        #
        #         new_component_list.add_subcomponent(new_val._wrapped_obj,
        #                                             slot_extension=str(i),
        #                                             slot=taxonomy_entry)

        # logger.debug(f'Created new component list {new_component_list.id} from values {new_component_list}')

        return new_component_list

    @property
    def components(self):
        return [x.Component for x in self._wrapped_obj.Components.Items]

    @property
    def ref_components(self):
        return [x.Target for x in self._wrapped_obj.ReferencedComponents.Items if x.Target is not None]

    @property
    def data(self) -> List[SimultanObject]:
        try:
            if self._wrapped_obj is None:
                return
            components = self.components
            ref_components = self.ref_components
            all_components = [*components, *ref_components]

            slots = [*[x.Slot for x in self._wrapped_obj.Components.Items],
                     *[x.Slot for x in self._wrapped_obj.ReferencedComponents.Items if x.Target is not None]]

            try:
                indices = sort_slots(slots)
                return [self._object_mapper.create_python_object(x, data_model=self._data_model) for x in
                        [all_components[i] for i in np.argsort(indices)]]
            except TypeError as e:
                logger.warning(f'Could not sort list {all_components}:\n{e}')
                return [self._object_mapper.create_python_object(x, data_model=self._data_model) for x in all_components]
        except Exception as e:
            logger.error(f'Could not get data from list {self}:\n{e}')
            return []

    def discard(self, value: SimultanObject):

        components = self.components
        subcomponents = self.ref_components

        if value._wrapped_obj in components:
            index = components.index(value._wrapped_obj)
            self.remove_subcomponent(value._wrapped_obj)
        elif value._wrapped_obj in subcomponents:
            index = subcomponents.index(value._wrapped_obj)
            self.remove_referenced_component(value._wrapped_obj)
        else:
            raise ValueError(f'Component {value} not in list {self}')
        self._update_slot_extensions(index)

    def append(self, values: Union[SimultanObject, List]):

        if not isinstance(values, Iterable):
            values = [values]

        for i, value in enumerate(values, start=len(self.data)):
            self._set_value(value, i)

    def _update_slot_extensions(self, index: int):

        # update slot extension of all elements > index
        for i, component in enumerate(self.data):
            if i > index-1:
                if component._wrapped_obj in self.components:
                    slot, c_entry = next((x.Slot, x) for x in self._wrapped_obj.Components.Items if x.Component == component._wrapped_obj)
                elif component._wrapped_obj in self.ref_components:
                    slot = next(x.Slot for x in self._wrapped_obj.ReferencedComponents.Items if x.Target == component._wrapped_obj)
                else:
                    raise ValueError(f'Component {component} not in list {self}')
                c_entry.set_Slot(SimSlot(slot.SlotBase, str(i)))

    def _set_value(self, value, i):

        if isinstance(value, SimultanObject):
            slot = value._wrapped_obj.Slots.Items[0]

            if self.component_policy == 'subcomponent' and value._wrapped_obj.Parent is None:
                self.add_subcomponent(value._wrapped_obj,
                                      slot_extension=str(i),
                                      slot=slot)
            else:
                self.add_referenced_component(value._wrapped_obj,
                                              slot_extension=str(i),
                                              slot=slot)
        else:
            new_val = create_mapped_python_object(value,
                                                  data_model=self._data_model,
                                                  object_mapper=self._object_mapper,
                                                  add_to_data_model=True)

            taxonomy = self._data_model.get_or_create_taxonomy(taxonomy_name=new_val._taxonomy_map.taxonomy_name,
                                                               taxonomy_key=new_val._taxonomy_map.taxonomy_key)

            taxonomy_entry = self._data_model.get_or_create_taxonomy_entry(name=new_val._taxonomy_map.taxonomy_entry_name,
                                                                           key=new_val._taxonomy_map.taxonomy_entry_key,
                                                                           sim_taxonomy=taxonomy)

            if new_val._wrapped_obj.Parent is None:
                self.add_subcomponent(new_val._wrapped_obj,
                                      slot_extension=str(i),
                                      slot=taxonomy_entry)
            else:
                self.add_referenced_component(new_val._wrapped_obj,
                                              slot_extension=str(i),
                                              slot=taxonomy_entry)

    def __setitem__(self, i, value):
        if isinstance(i, slice):
            for j, val in enumerate(value):
                self.__setitem__(i.start + j, val)
        else:
            if i < 0:
                i += len(self.data)

            if i >= len(self.data):
                self.append([value])
            else:
                if self.data[i] is value:
                    return
                self.discard(self.data[i])
                self._set_value(value, i)

    def extend(self, values: List):
        self.append(values)

    def remove(self, value: SimultanObject):
        self.discard(value)

    def add(self, value: Union[SimultanObject, List[SimultanObject]]):
        if value not in self.data:
            self.append(value)

    def move_item(self, item: SimultanObject, new_index: int):
        if item not in self.data:
            raise ValueError(f'Item {item} not in list {self}')
        old_index = self.data.index(item)

        if new_index < 0:
            new_index += len(self.data)

        if new_index == old_index:
            return

        new_data = self.data.copy()
        new_data.pop(old_index)
        new_data.insert(new_index, item)

        for i, item in enumerate(new_data):
            if item._wrapped_obj in self.components:
                slot, c_entry = next(
                    (x.Slot, x) for x in self._wrapped_obj.Components.Items if x.Component == item._wrapped_obj)
            elif item._wrapped_obj in self.ref_components:
                slot = next(
                    x.Slot for x in self._wrapped_obj.ReferencedComponents.Items if x.Target == item._wrapped_obj)
            else:
                raise ValueError(f'Component {item} not in list {self}')
            c_entry.set_Slot(SimSlot(slot.SlotBase, str(i)))

    def __getitem__(self, i):
        if isinstance(i, slice):
            if self._object_mapper is None:
                return self.__class__(self.data[i])
            return [self._object_mapper.create_python_object(x, data_model=self._data_model)
                    for x in self.__class__(self.data[i])]
        else:
            if self._object_mapper is None:
                return self.data[i]
            return self._object_mapper.create_python_object(self.data[i], data_model=self._data_model)

    def __repr__(self):
        return f'List {self.name}: ' + repr(list(self.data))

    def __iter__(self):
        return iter([self._object_mapper.create_python_object(x, data_model=self._data_model) for x in self.data])

    def __next__(self):
        try:
            result = self.__getitem__(self.index)
        except IndexError:
            raise StopIteration
        self.index += 1
        return result

    def __len__(self):
        return self.data.__len__()

    @property
    def parent(self):
        if not hasattr(self._wrapped_obj, 'Parent'):
            return None

        if self._wrapped_obj.Parent is not None:
            return self._object_mapper.create_python_object(self._wrapped_obj.Parent, data_model=self._data_model)
        else:
            return None

    @property
    def referenced_by(self):
        return set([self._object_mapper.create_python_object(x.Target, data_model=self._data_model) for x in self._wrapped_obj.ReferencedBy if
                    x.Target != self._wrapped_obj])

    def clear(self):
        self._wrapped_obj.Components.Clear()
        self._wrapped_obj.ReferencedComponents.Clear()


component_list_map = TaxonomyMap(taxonomy_name='PySimultan',
                                 taxonomy_key='PySimultan',
                                 taxonomy_entry_name='ComponentList',
                                 taxonomy_entry_key='ComponentList',
                                 )

ComponentList._taxonomy_map = component_list_map


class ComponentDictionary(SimultanObject):

    component_policy = 'subcomponent'  # component add policy of the content/parameter/property, 'reference'
    # or 'subcomponent'

    type_setter_fcn_lookup_dict = {None: lambda x: None,
                                   SimComponent: set_property_to_sim_component,
                                   SimultanObject: set_property_to_sim_component,
                                   SimDoubleParameter: set_property_to_parameter,
                                   SimIntegerParameter: set_property_to_parameter,
                                   SimStringParameter: set_property_to_parameter,
                                   SimBoolParameter: set_property_to_parameter,
                                   SimEnumParameter: set_property_to_parameter,
                                   int: set_property_to_parameter,
                                   float: set_property_to_parameter,
                                   str: set_property_to_parameter,
                                   bool: set_property_to_parameter,
                                   FileInfo: set_property_to_file_info,
                                   list: set_property_to_list,
                                   tuple: set_property_to_list,
                                   set: set_property_to_list,
                                   dict: set_property_to_dict,
                                   ComponentList: set_property_to_list,
                                   np.ndarray: set_property_to_value_field,
                                   pd.DataFrame: set_property_to_value_field}

    _taxonomy_map = TaxonomyMap(taxonomy_name='Dictionaries',
                                taxonomy_key='Dictionaries',
                                taxonomy_entry_name='ComponentDict',
                                taxonomy_entry_key='ComponentDict',
                                )

    _taxonomy = 'ComponentDict'

    def __init__(self, *args, **kwargs):
        self._dict = {}
        super().__init__(*args, **kwargs)
        self.component_policy = kwargs.get('component_policy', 'subcomponent')  # component add policy of the content/parameter/property, 'reference' or 'subcomponent'

    @classmethod
    def create_from_values(cls,
                           values: dict[str, Any],
                           data_model=None,
                           object_mapper=None,
                           *args,
                           **kwargs,
                           ):

        wrapped_obj = create_simultan_component_for_taxonomy(cls,
                                                             data_model=data_model,
                                                             object_mapper=object_mapper,
                                                             add_to_data_model=kwargs.get('add_to_data_model', True))

        new_component_dict = cls(wrapped_obj=wrapped_obj,
                                 data_model_id=data_model.id,
                                 object_mapper=object_mapper,
                                 data_model=data_model,
                                 )

        wrapped_obj.Name = kwargs.get('name', 'UnnamedComponentDict')

        for key, value in values.items():
            new_component_dict[key] = value

        return new_component_dict

    def __getitem__(self, key, *args, **kwargs):

        comp_dict = object.__getattribute__(self, '_dict')

        if kwargs.get('check_dict', True) and comp_dict is not None and key in object.__getattribute__(self,
                                                                                                       '_dict').keys():
            return object.__getattribute__(self, '_dict')[key]
        else:
            # data_model = config.default_data_model
            obj = get_component_taxonomy_entry(self._wrapped_obj, key)
            if obj is not None:
                val = get_obj_value(obj, data_model=self._data_model, object_mapper=self._object_mapper)
                self._dict[key] = val
        return self._dict[key]

    def __setitem__(self, key, value):

        if key in self._dict:
            del self._dict[key]

        if key in self._taxonomy_map.content_dict.keys():
            content = self._taxonomy_map.content_dict[key]
        else:
            content = Content(text_or_key=key,
                              property_name=key,
                              type=None,
                              unit=None,
                              documentation=f'Property {key} in ComponentDictionary',
                              component_policy=self.component_policy)
            self._taxonomy_map.add_content(content)
        taxonomy_entry = content.get_taxonomie_entry(self._data_model)

        component_idx, ref_component_idx, parameter_idx, ref_asset_idx = get_param_indices(self._wrapped_obj,
                                                                                           taxonomy_entry)

        slot_extension = content.slot_extension

        if slot_extension is None:
            slot_extension = 0

        fcn_arg_list = [value,
                        self,
                        key,
                        taxonomy_entry,
                        slot_extension,
                        component_idx,
                        ref_component_idx,
                        parameter_idx,
                        ref_asset_idx,
                        content]

        if value is None:
            remove_prop_from_sim_component(component=self._wrapped_obj,
                                           component_idx=component_idx,
                                           ref_component_idx=ref_component_idx,
                                           parameter_idx=parameter_idx,
                                           keep=[])

        if isinstance(value, (list, tuple, set, ComponentList)):
            setter_fcn = set_property_to_list
        elif isinstance(value, SimultanObject):
            setter_fcn = set_property_to_sim_component
        else:
            setter_fcn = self.type_setter_fcn_lookup_dict.get(type(value), set_property_to_unknown_type)

        setter_fcn(*fcn_arg_list)
        item = self.__getitem__(key, check_dict=False)

        # self._object_mapper.create_python_object(self._wrapped_obj)
        #
        # if isinstance(value, ):

        self._dict[key] = self.__getitem__(key, check_dict=False)

    def __delitem__(self, key):
        self[key] = None
        del self._dict[key]

    def items(self):
        return self._dict.items()

    def keys(self):
        if not self._dict:
            self._generate_internal_dict()
        return self._dict.keys()

    def values(self):
        if not self._dict:
            self._generate_internal_dict()
        return self._dict.values()

    def _generate_internal_dict(self):
        comp_dict = {}

        for parameter in self._wrapped_obj.Parameters.Items:
            comp_dict[parameter.NameTaxonomyEntry.TextOrKey] = get_obj_value(parameter,
                                                                             data_model=self._data_model,
                                                                             object_mapper=self._object_mapper)
        for component in self._wrapped_obj.Components.Items:
            comp_dict[component.Slot.SlotBase.Target.Key] = get_obj_value(component.Component,
                                                                          data_model=self._data_model,
                                                                          object_mapper=self._object_mapper)
        for ref_component in self._wrapped_obj.ReferencedComponents.Items:
            comp_dict[ref_component.Slot.SlotBase.Target.Name] = get_obj_value(ref_component.Target,
                                                                               data_model=self._data_model,
                                                                               object_mapper=self._object_mapper)
        for ref_asset in self._wrapped_obj.ReferencedAssets.Items:
            for tag in ref_asset.Resource.Tags:
                comp_dict[tag.Target.Key] = get_obj_value(ref_asset.Target,
                                                          data_model=self._data_model,
                                                          object_mapper=self._object_mapper)

        object.__setattr__(self, '_dict', comp_dict)

    def clear(self):
        for key in self.keys():
            del self[key]

    def __repr__(self):
        if not self._dict:
            self._generate_internal_dict()
        return repr(self._dict)

    def __iter__(self):
        return self._dict.__iter__()

    def __next__(self):
        return self._dict.__next__()

    def __len__(self):
        return len(self._dict)

    def __contains__(self, key):
        return key in self._dict

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def update(self, other):
        for key, value in other.items():
            self[key] = value


component_dict_map = ComponentDictionary._taxonomy_map
