import sys
import colorlog
from .config import *
from .data_model import DataModel
from .files import FileInfo
from .object_mapper import PythonMapper

# from .simultan_utils import create_component
# from .template_tools import Template, TemplateParser
# from .geo_default_types import BaseGeometricLayer, BaseGeometricVertex, BaseGeometricEdge, BaseGeometricEdgeLoop, BaseGeometricFace, BaseGeometricVolume
#
# print(sys.version)
#
# from ParameterStructure.Components import SimComponent
# from ParameterStructure.Parameters import SimParameter

# from .utils import create_component

handler = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)

handler.setFormatter(formatter)

logger = colorlog.getLogger('PySimultan')
logger.addHandler(handler)
