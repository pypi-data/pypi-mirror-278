from PySimultan2.data_model import DataModel
from PySimultan2.object_mapper import PythonMapper
from PySimultan2.taxonomy_maps import TaxonomyMap, Content

import resources

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 importlib_resources.
    import importlib_resources as pkg_resources


with pkg_resources.path(resources, 'test_set_dictionary.simultan') as r_path:
    project_path = str(r_path)

data_model = DataModel.create_new_project(project_path=project_path,
                                          user_name='admin',
                                          password='admin')

mapper = PythonMapper()


def map_classes():
    class TestComponent(object):
        def __init__(self, *args, **kwargs):
            self.mapped_property = kwargs.get('mapped_property')
            self.value2 = kwargs.get('value2')

    content0 = Content(text_or_key='value',  # text or key of the content/parameter/property
                       property_name='mapped_property',  # name of the generated property
                       type=None,  # type of the content/parameter/property
                       unit=None,  # unit of the content/parameter/property
                       documentation='mapped_property to test',
                       component_policy='subcomponent')

    content1 = Content(text_or_key='value2',  # text or key of the content/parameter/property
                       property_name='value2',  # name of the generated property
                       type=None,  # type of the content/parameter/property
                       unit=None,  # unit of the content/parameter/property
                       documentation='value2',
                       component_policy='reference')

    test_component_map = TaxonomyMap(taxonomy_name='PySimultan',
                                     taxonomy_key='PySimultan',
                                     taxonomy_entry_name='TestComponent',
                                     taxonomy_entry_key='TestComponent',
                                     content=[content0, content1],
                                     )

    mapper.register(test_component_map.taxonomy_entry_key, TestComponent, taxonomy_map=test_component_map)
    cls1 = mapper.get_mapped_class(test_component_map.taxonomy_entry_key)

    test_component_map_2 = TaxonomyMap(taxonomy_name='PySimultan',
                                       taxonomy_key='PySimultan',
                                       taxonomy_entry_name='TestComponent2',
                                       taxonomy_entry_key='TestComponent2',
                                       content=[content0],
                                       )

    mapper.register(test_component_map_2.taxonomy_entry_key, TestComponent, taxonomy_map=test_component_map_2)
    cls2 = mapper.get_mapped_class(test_component_map_2.taxonomy_entry_key)

    return cls1, cls2


mapped_cls_1, mapped_cls_2 = map_classes()
component = mapped_cls_1(name='test_component',
                         mapped_property=None)


def test_set_dictionary_param(component):
    test_dict = {'val_a': 1,
                 'val_b': 2.0,
                 'val_c': 'test'}
    component.mapped_property = test_dict

    component.mapped_property['val_a'] = 222

    print(component.mapped_property)


if __name__ == '__main__':
    test_set_dictionary_param(component)
    data_model.save()

data_model.cleanup()
print('Test passed')
