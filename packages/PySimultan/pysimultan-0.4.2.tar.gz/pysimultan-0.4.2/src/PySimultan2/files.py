"""
This module contains classes and functions to handle files and directories.
"""
from __future__ import annotations
from datetime import datetime

import contextlib
import os
import io
import shutil
import tempfile
from typing import List, Union, Optional
import shutil
import zipfile
# from System.IO import FileInfo  # public FileInfo (string fileName);

from SIMULTAN.Data.Assets import ResourceEntry, ResourceFileEntry, ContainedResourceFileEntry, Asset
from SIMULTAN.Data.Taxonomy import SimTaxonomyEntry, SimTaxonomyEntryReference, SimTaxonomy
from SIMULTAN.Data.Components import SimComponent, ComponentMapping

# from .config import default_data_model

from . import config, logger

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .data_model import DataModel
    from .simultan_object import SimultanObject


@contextlib.contextmanager
def cd(newdir, cleanup=lambda: True):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
        cleanup()


@contextlib.contextmanager
def tempdir():
    dir_path = tempfile.mkdtemp()

    def cleanup():
        shutil.rmtree(dir_path)

    with cd(dir_path, cleanup):
        yield dir_path


def add_tag_to_resource(resource: Union[ResourceFileEntry, ContainedResourceFileEntry],
                        tag: Union[SimTaxonomyEntry, SimTaxonomyEntryReference]):
    """
    Add a tag to an asset.

    :param resource: The resource to add the tag to.
    :param tag: The tag to add to the asset.
    :return: None
    """
    if isinstance(tag, SimTaxonomyEntry):
        tag = SimTaxonomyEntryReference(tag)

    if tag not in resource.Tags:
        resource.Tags.Add(tag)


def add_asset_to_component(comp: [SimComponent, SimultanObject],
                           asset: Union[ResourceFileEntry, ContainedResourceFileEntry],
                           content_id: str = '',
                           tag: SimTaxonomyEntry = None) -> Asset:
    """
    Add an asset to a component with a content id.
    :param comp: Component to add the asset; ParameterStructure.Components.SimComponent
    :param asset: Asset to be added; ParameterStructure.Assets.ResourceFileEntry
    :param content_id: Content id of the asset; string; E.g. '0' as the page of a pdf
    :param tag: Tag to be added to the asset.
    :return:
    """
    wrapped_obj = comp if isinstance(comp, SimComponent) else comp._wrapped_obj

    if tag is not None:
        add_tag_to_resource(asset, tag)

    return ComponentMapping.AddAsset(wrapped_obj, asset, content_id)


def remove_asset_from_component(comp: Union[SimComponent, SimultanObject],
                                asset: Asset) -> None:
    """
    Remove an asset from a component with a content id.
    :param comp: Component to remove the asset from; ParameterStructure.Components.SimComponent
    :param asset:
    :return:
    """
    wrapped_obj = comp if isinstance(comp, SimComponent) else comp._wrapped_obj
    return ComponentMapping.RemoveAsset(wrapped_obj, asset)


def create_asset_from_string(filename: str,
                             content: str,
                             data_model: DataModel,
                             tag: Optional[Union[SimTaxonomyEntry, SimTaxonomyEntryReference]] = None) -> ResourceFileEntry:
    """
    Create a new asset from a string. The asset is added to the data model.
    :param filename: Name of the file to be created. E.g. 'new_file.txt'
    :param content:  Content of the file. E.g. 'This is the content of the file.'
    :param data_model:  Data model to add the asset to.
    :param tag: Tag to be added to the asset.
    :return: ResourceFileEntry
    """
    with tempdir() as dirpath:
        filepath = os.path.join(dirpath, filename)
        with open(filepath, 'w') as f:
            f.write(content)

        resource = data_model.add_resource(filepath)

    if tag is not None:
        add_tag_to_resource(resource, tag)

    return resource


def create_asset_from_str_io(filename: str,
                             content: io.StringIO,
                             data_model: DataModel,
                             tag: Union[SimTaxonomyEntry, SimTaxonomyEntryReference] = None) -> ResourceFileEntry:
    """
    Create a new asset from a string io. The asset is added to the data model.
    :param filename: Name of the file to be created. E.g. 'new_file.txt'
    :param content:  Content of the file. E.g. 'This is the content of the file.'
    :param data_model:  Data model to add the asset to.
    :param tag: Tag to be added to the asset.
    :return: ResourceFileEntry
    """
    with tempdir() as dirpath:
        filepath = os.path.join(dirpath, filename)
        with open(filepath, 'w') as f:
            f.write(content.getvalue())

        resource = data_model.add_resource(filepath)

    if tag is not None:
        add_tag_to_resource(resource, tag)

    return resource


def create_asset_from_file(file_info: FileInfo,
                           data_model: DataModel,
                           tag: Union[SimTaxonomyEntry, SimTaxonomyEntryReference] = None) -> Union[
                           ResourceFileEntry, ContainedResourceFileEntry]:
    """
    Create a new asset from a file. The asset is added to the data model.
    :param file_info: FileInfo object of the file to be added.
    :param data_model:  Data model to add the asset to.
    :param tag: Tag to be added to the asset.
    :return: ResourceFileEntry
    """
    resource = data_model.add_resource(file_info.file_path)

    if tag is not None:
        add_tag_to_resource(resource, tag)

    return resource


class MetaMock(type):
    def __call__(cls, *args, **kwargs):
        resource_entry = kwargs.get('resource_entry', None)
        if resource_entry is not None and hasattr(resource_entry, 'Key'):
            obj = cls._cls_instances.get(resource_entry.Key, None)
            if obj is not None:
                return obj

        obj = cls.__new__(cls)
        obj.__init__(*args, **kwargs)
        if obj.resource_entry is not None:
            cls._cls_instances[obj.resource_entry.Key] = obj
        return obj


class FileInfo(object, metaclass=MetaMock):

    _cls_instances = {}

    @classmethod
    def from_string(cls, filename: str, content: str, *args, **kwargs) -> FileInfo:
        """
        Create a file info object from a string.
        :param filename: Name of the file to be created. E.g. 'new_file.txt'
        :param content:  Content of the file. E.g. 'This is the content of the file.'
        :param args:
        :param kwargs:
        :return: FileInfo
        """

        data_model = kwargs.get('data_model', config.get_default_data_model())
        resource = create_asset_from_string(filename, content, *args, **kwargs)

        file_info = cls(resource_entry=resource,
                        data_model=data_model)
        file_info.write_content(content)
        return file_info

    def __init__(self, file_path=None, *args, **kwargs):
        """
        Custom file info object to be used with the with statement. This object is used to open a file and close it
        automatically.
        Example:

        file_path = 'path/to/file.txt'
        file_info = FileInfo(file_path, 'r')

        with file_info as f:
            print(f.read())

        :param file_path:
        :param args:
        :param kwargs:
        """
        # do custom stuff here
        self._resource_entry: Union[ResourceFileEntry, ContainedResourceFileEntry, None] = None

        if file_path is not None:
            self.file_path: str = file_path
        else:
            self.file_path = kwargs.get('resource_entry').File.FullPath

        self.data_model: Union[DataModel, None] = kwargs.get('data_model', None)
        self.resource_entry = kwargs.get('resource_entry', None)

        self.encoding = kwargs.get('encoding', 'utf-8')

        self.args = args
        self.kwargs = kwargs

    @property
    def resource_entry(self) -> Union[ResourceFileEntry, ContainedResourceFileEntry, None]:
        if self._resource_entry is None:
            if self.data_model is None:
                logger.warning(f'No data model provided. Using default data model: {config.get_default_data_model().id}.')
                self.data_model = config.get_default_data_model()
            if self.data_model is not None:
                self.resource_entry = self.data_model.add_resource(self.file_path)
        return self._resource_entry

    @resource_entry.setter
    def resource_entry(self, value):

        if value is not None:
            self._cls_instances[value.Key] = self
        else:
            del self._cls_instances[self._resource_entry.Key]
        self._resource_entry = value

    @property
    def file_size(self) -> int:
        return os.path.getsize(self.file_path)

    @property
    def last_modified(self) -> datetime:
        return datetime.fromtimestamp(os.path.getmtime(self.file_path))

    @resource_entry.setter
    def resource_entry(self, value):
        self._resource_entry = value

    @property
    def name(self) -> str:
        return os.path.basename(self.file_path)

    @name.setter
    def name(self, value: str):
        os.rename(self.file_path, os.path.join(os.path.dirname(self.file_path), value))
        self.file_path = os.path.join(os.path.dirname(self.file_path), value)

    @property
    def full_path(self) -> str:
        return os.path.abspath(self.file_path)

    @property
    def size(self) -> int:
        return os.path.getsize(self.file_path)

    @property
    def is_zip(self) -> bool:
        return self.file_path.endswith('.zip')

    @property
    def files(self) -> List[str]:
        if self.is_zip:
            with zipfile.ZipFile(self.file_path, 'r') as z:
                return z.namelist()
        else:
            return []

    @property
    def exists(self) -> bool:
        return os.path.exists(self.file_path)

    @property
    def content(self) -> str:
        return self.get_content(encoding=self.encoding)

    @content.setter
    def content(self, value: str):
        self.write_content(value)

    def __enter__(self):
        self.file_obj = open(self.file_path, *self.args, **self.kwargs)
        return self.file_obj

    def __exit__(self, *args):
        self.file_obj.close()

    def get_content(self, encoding='utf-8') -> Optional[Union[str, dict[str, str]]]:
        """
        Get the content of the file.
        :param encoding: Encoding of the file.
        :return: File content
        """
        if self.exists:
            if self.file_path.endswith('.zip'):
                content = {}
                with zipfile.ZipFile(self.file_path, 'r') as z:
                    for file in z.namelist():
                        content[file] = z.read(file).decode(encoding)
                return content
            else:
                with open(self.file_path, 'r', encoding=encoding) as f:
                    return f.read()
        else:
            return

    def copy(self, new_file_path: Optional) -> FileInfo:
        """
        Copy the file to a new location.
        :param new_file_path: New file path.
        :return: FileInfo
        """
        shutil.copy(self.full_path, new_file_path)
        return FileInfo(new_file_path)

    def write_content(self, content: str, encoding='utf-8') -> None:
        """
        Write content to the file.
        :param content: Content to be written to the file.
        :param encoding: Encoding of the file.
        :return: None
        """
        with open(self.file_path, 'w', encoding=encoding) as f:
            f.write(content)

    def append_content(self, content: str, encoding='utf-8') -> None:
        """
        Append content to the file.
        :param content: Content to be appended to the file.
        :param encoding: Encoding of the file.
        :return: None
        """
        with open(self.file_path, 'a', encoding=encoding) as f:
            f.write(content)

    def delete(self) -> None:
        """
        Delete the file.
        :return: None
        """
        if self.resource_entry is not None:
            self.data_model.delete_resource(self.resource_entry)
        os.remove(self.file_path)
