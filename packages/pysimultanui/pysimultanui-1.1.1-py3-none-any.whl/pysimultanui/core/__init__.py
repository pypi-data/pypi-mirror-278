from typing import Union
from .user import UserManager

from PySimultan2.object_mapper import PythonMapper
from PySimultan2.data_model import DataModel
from .method_mapper import method_mapper, mapped_method
from .logging import logger

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..app.home import ProjectManager
    from ..views.view_manager import ViewManager
    from ..views.geometry_view import GeometryManager
    from .navigation import Navigation
    from ..views.asset_view import AssetManager


mapper = PythonMapper()
method_mapper.mapper = mapper
mapper.method_mapper = method_mapper

# data_model: Union[DataModel, None] = None
# navigation: Union['Navigation', None] = None
# view_manager: Union['ViewManager', None] = None
# project_manager: Union['ProjectManager', None] = None
# asset_manager: Union['AssetManager', None] = None
# geometry_manager: Union['GeometryManager', None] = None
#
# navigation_drawer = None
# project_tab = None
# detail_view = None
# home_tab = None
