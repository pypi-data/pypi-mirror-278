import os
import sys
from ruamel.yaml import YAML, yaml_object, add_representer

import colorlog
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 importlib_resources.
    import importlib_resources as pkg_resources


from . import resources
sys.path.append(str(pkg_resources.files(resources)))

logger = colorlog.getLogger('PySimultan')
logger.setLevel('DEBUG')

dll_path = os.environ.get('SIMULTAN_SDK_DIR', None)
if dll_path is None:
    with pkg_resources.path(resources, 'SIMULTAN.dll') as r_path:
        dll_path = str(r_path)
sys.path.append(dll_path)

from pythonnet import load
from pythonnet import clr_loader, set_runtime
list(clr_loader.find_runtimes())
load('coreclr')
import clr
test = clr.AddReference(os.path.join(dll_path, 'SIMULTAN.dll') if not dll_path.endswith('SIMULTAN.dll') else dll_path)
clr.AddReference("System.Security.Cryptography")
# clr.AddReference(os.path.join(dll_path, 'SIMULTAN'))

from SIMULTAN.Data.Components import SimComponent

continue_on_error = True


def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')


add_representer(type(None), represent_none)
yaml = YAML()
yaml.default_flow_style = None
yaml.preserve_quotes = True
yaml.allow_unicode = True

# define which axis is in up/down direction; 0: x-axis; 1: y-axis; 2: z-axis; In SIMULTAN the y-axis is the up/down axis
cs_axis_up = 2
default_data_model = None
default_mapper = None
