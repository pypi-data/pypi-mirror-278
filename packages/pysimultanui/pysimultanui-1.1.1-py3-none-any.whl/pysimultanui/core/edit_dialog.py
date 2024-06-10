from nicegui import ui, app

from numpy import ndarray

from .. import user_manager
from ..core.user import User
from .. import core
from PySimultan2.simultan_object import SimultanObject
from PySimultan2.files import FileInfo
from PySimultan2.multi_values import simultan_multi_value_field_3d_to_numpy
from ..config import logger
from math import inf

from SIMULTAN.Data.MultiValues import (SimMultiValueField3D, SimMultiValueField3DParameterSource, SimMultiValueBigTable,
                                       SimMultiValueBigTableHeader, SimMultiValueBigTableParameterSource)



def get_value_content_type(value):
    if value is None:
        return 'None'
    if isinstance(value, str):
        return 'str'
    elif isinstance(value, int):
        return 'int'
    elif isinstance(value, float):
        return 'float'
    elif isinstance(value, SimultanObject):
        return 'Component'
    else:
        return 'None'


class ParameterEditDialog(object):

    def __init__(self, *args, **kwargs):
        self.sim_parameter = kwargs.get('sim_parameter', None)


class IntEditDialog(ParameterEditDialog):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.value_input = None
        self.min_input = None
        self.max_input = None
        self.unit_input = None

    def ui_content(self):
        with ui.row():
            self.value_input = ui.input(value=self.sim_parameter.Value if self.sim_parameter is not None else 0,
                                        validation=self.validate, label='Value')
            self.min_input = ui.input(value=self.sim_parameter.ValueMin if self.sim_parameter is not None else -inf,
                                      validation=self.validate, label='Min. Value')
            self.max_input = ui.input(value=self.sim_parameter.ValueMax if self.sim_parameter is not None else inf,
                                      validation=self.validate, label='Max. Value')
            self.unit_input = ui.input(value=self.sim_parameter.Unit if self.sim_parameter is not None else '',
                                       label='Unit')

    @staticmethod
    def validate(value):
        try:
            int(value)
        except ValueError:
            return "Value must be an integer!"

    @property
    def value(self):
        return int(self.value_input.value)

    @property
    def min(self):
        return int(self.min_input.value) if self.min_input.value != '-inf' else -inf

    @property
    def max(self):
        return int(self.max_input.value) if self.max_input.value != 'inf' else inf

    @property
    def unit(self):
        return self.unit_input.value


class FloatEditDialog(IntEditDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def validate(value):
        try:
            float(value)
        except ValueError:
            return "Value must be an float!"

    @property
    def value(self):
        return float(self.value_input.value)

    @property
    def min(self):
        return float(self.min_input.value)

    @property
    def max(self):
        return float(self.max_input.value)


class StrEditDialog(ParameterEditDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value_input = None

    def ui_content(self):
        with ui.row():
            self.value_input = ui.input(value=self.sim_parameter.Value if self.sim_parameter is not None else '')

    @property
    def value(self):
        return self.value_input.value


class ComponentEditDialog(object):

    def __init__(self, *args, **kwargs):
        self.select_multiple = kwargs.get('select_multiple', True)
        self.component = kwargs.get('component', None)
        self.content = kwargs.get('content', None)
        self.parent = kwargs.get('parent', None)
        self.dialog = None

        self.class_select = None
        self.component_select = None

        self.component_name_map: dict = {}

    @property
    def value(self):
        if len(self.component_select.value) == 0:
            return None
        elif __len__ := len(self.component_select.value) == 1:
            return self.component_name_map[self.component_select.value[0]]
        else:
            return [self.component_name_map[x] for x in self.component_select.value]

    @ui.refreshable
    def ui_content(self):
        with ui.card():
            ui.label('Select component')
            mapper = user_manager[app.storage.user['username']].mapper
            classes = mapper.mapped_classes

            if isinstance(self.component, SimultanObject):
                select_value = self.component._taxonomy
            else:
                select_value = 'All'

            self.class_select = ui.select(['All', *classes.keys()],
                                          label='Select class',
                                          value=[select_value],
                                          multiple=self.select_multiple,
                                          on_change=self.on_cls_change,
                                          with_input=True
                                          ).classes('w-full').props('use-chips')
            self.component_ui_content()

    @ui.refreshable
    def component_ui_content(self):

        components = []
        self.component_name_map = {}

        mapper = user_manager[app.storage.user['username']].mapper

        if 'All' in self.class_select.value:
            for cls in mapper.mapped_classes.values():
                components.extend(cls.cls_instances)
        else:
            if isinstance(self.class_select.value, str):
                selected_val = [self.class_select.value]
            else:
                selected_val = self.class_select.value

            for cls in [mapper.get_mapped_class(x) for x in selected_val]:
                components.extend(cls.cls_instances)

        for component in components:
            self.component_name_map[f'{component.name} ({component.id})'] = component

        if isinstance(self.component, SimultanObject):
            select_value = [f'{self.component.name} ({self.component.id})']
        else:
            select_value = []

        self.component_select = ui.select(list(self.component_name_map.keys()),
                                          label='Select component',
                                          value=select_value,
                                          multiple=True,
                                          with_input=True,
                                          on_change=self.on_component_change
                                          ).classes('w-64').props('use-chips')

    def on_cls_change(self, event):
        self.component_ui_content.refresh()

    def on_component_change(self, event):
        pass


class AssetEditDialog(object):

    def __init__(self, *args, **kwargs):

        self.asset_select = None

        asset = kwargs.get('asset', None)

        self.asset = asset if isinstance(asset, FileInfo) else None
        self.content = kwargs.get('content', None)
        self.parent = kwargs.get('parent', None)
        self.dialog = None

        self.asset_name_map = {}

    def ui_content(self):
        with ui.card():
            ui.label('Select asset')
            assets = user_manager[app.storage.user['username']].asset_manager.items
            self.asset_name_map = {x.name: x for x in assets}
            self.asset_select = ui.select([x.name for x in assets],
                                          label='Select asset',
                                          value=self.asset.name if self.asset is not None else None,
                                          on_change=self.asset_select,
                                          with_input=True
                                          ).classes('w-64').props('use-chips')

    @property
    def value(self):
        if len(self.asset_select.value) == 0:
            return None

        return self.asset_name_map[self.asset_select.value]


class ArrayEditDialog(object):

    def __init__(self, *args, **kwargs):
        self.array_select = None
        asset = kwargs.get('array', None)

        self.array: SimMultiValueField3D = asset if isinstance(asset, ndarray) else None
        self.content = kwargs.get('content', None)
        self.parent = kwargs.get('parent', None)
        self.dialog = None

        self.array_name_map = {}

    @property
    def user(self) -> User:
        return user_manager[app.storage.user['username']]

    def ui_content(self):
        with ui.card():
            ui.label('Select Array')
            arrays = self.user.array_manager.np_items
            self.array_name_map = {x.Name: x for x in arrays.values()}
            self.array_select = ui.select([x.Name for x in arrays.values()],
                                          label='Select asset',
                                          value=self.array.Name if self.array is not None else None,
                                          on_change=self.array_select,
                                          with_input=True
                                          ).classes('w-64').props('use-chips')

    @property
    def value(self):
        if len(self.array_select.value) == 0:
            return None

        return self.array_name_map[self.array_select.value]


default_options = ['None', 'str', 'int', 'float', 'bool', 'Component', 'Asset', 'Array', 'Table']


class ContentTypeChooser(object):

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.get('content_type', str)
        self.select = None
        self.value = None
        self.options = kwargs.get('options', default_options)

        self.on_change = kwargs.get('on_change', None)

    def ui_content(self):
        self.select = ui.select(self.options,
                                value=self.content_type,
                                label='Content type',
                                on_change=self.on_change).classes('w-full')

    def on_change(self, event):
        if self.on_change is not None:
            self.on_change(event, self.value)


class ContentEditDialog(object):

    def __init__(self, *args, **kwargs):

        self._options = None

        self.select_multiple = kwargs.get('select_multiple', True)
        self.component = kwargs.get('component', None)
        self.raw_val = kwargs.get('raw_val', None)
        self.parent = kwargs.get('parent', None)
        self.content = kwargs.get('content', None)
        self.taxonomy = kwargs.get('taxonomy', None)
        self.object_mapper = kwargs.get('object_mapper', None)
        self.dialog = None

        if self.component is not None:
            val_type = get_value_content_type(self.component)
        else:
            val_type = 'None'

        self.content_type = ContentTypeChooser(on_change=self.on_type_change,
                                               content_type=val_type,
                                               options=self.options)

        self.options = kwargs.get('options', default_options)

        self.edit_dialog = None

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options = value
        if self.content_type is not None:
            self.content_type.options = value

    def create_edit_dialog(self):
        with ui.dialog() as self.dialog, ui.card():
            # ui.label(f'Edit {self.content.name}')
            self.content_type.ui_content()
            self.ui_content()
            with ui.row():
                ui.button('Save', on_click=self.save)
                ui.button('Cancel', on_click=self.close)
            self.dialog.open()

    @ui.refreshable
    def ui_content(self):
        if self.content_type.select.value == 'str':
            self.edit_dialog = StrEditDialog(sim_parameter=self.raw_val)
            self.edit_dialog.ui_content()
        elif self.content_type.select.value == 'int':
            self.edit_dialog = IntEditDialog(sim_parameter=self.raw_val)
            self.edit_dialog.ui_content()
        elif self.content_type.select.value == 'float':
            self.edit_dialog = FloatEditDialog(sim_parameter=self.raw_val)
            self.edit_dialog.ui_content()
        elif self.content_type.select.value == 'Component':
            self.edit_dialog = ComponentEditDialog(component=self.component,
                                                   content=self.content,
                                                   parent=self.parent,
                                                   select_multiple=self.select_multiple)
            self.edit_dialog.ui_content()
        elif self.content_type.select.value == 'Asset':
            self.edit_dialog = AssetEditDialog(asset=self.component,
                                               content=self.content,
                                               parent=self.parent)
            self.edit_dialog.ui_content()
        elif self.content_type.select.value == 'Array':
            self.edit_dialog = ArrayEditDialog(array=self.component,
                                               content=self.content,
                                               parent=self.parent)
            self.edit_dialog.ui_content()
        else:
            ui.label('Not implemented content type!')

    def on_type_change(self):
        self.ui_content.refresh()

    def close(self, *args, **kwargs):
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None

    def save(self, *args, **kwargs):

        setattr(self.parent.component, self.content.property_name, self.edit_dialog.value)
        if self.content_type.select.value in ['int', 'float']:
            if self.raw_val is None:
                self.raw_val = self.parent.component.get_raw_attr(self.content.property_name)
            setattr(self.raw_val, 'ValueMin', self.edit_dialog.min)
            setattr(self.raw_val, 'ValueMax', self.edit_dialog.max)
            setattr(self.raw_val, 'Unit', self.edit_dialog.unit)

        logger.info(f'Updated {self.content.name} to {self.edit_dialog.value}')

        if self.parent is not None:
            self.parent.refresh()
        self.close()

        from ..views.detail_views import show_detail
        show_detail(value=self.parent.component)


class DictEditDialog(object):

    def __init__(self, *args, **kwargs):
        self.component = kwargs.get('component', None)
        self._key = None

        self.parent = kwargs.get('parent', None)
        self.dialog = None

        self.key_edit = None
        self.edit_dialog = None
        self.key = kwargs.get('key', None)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value
        if self.key_edit is not None:
            self.key_edit.value = value

    def create_edit_dialog(self):
        with ui.dialog() as self.dialog, ui.card():
            ui.label(f'Edit {self.key}')
            self.ui_content()
            with ui.row():
                ui.button('Save', on_click=self.save)
                ui.button('Cancel', on_click=self.close)
            self.dialog.open()

    @ui.refreshable
    def ui_content(self):
        self.key_edit = ui.input(value=self.key, label='Key', on_change=self.on_key_change)
        self.edit_dialog = ContentEditDialog(component=getattr(self.parent.component, self.key) if self.key is not None else None,
                                             content=None,
                                             parent=self.parent,
                                             select_multiple=False)
        self.edit_dialog.content_type.ui_content()
        self.edit_dialog.ui_content()

    def on_key_change(self, event):
        self.key = self.key_edit.value

    def close(self, *args, **kwargs):
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None

    def save(self, *args, **kwargs):
        setattr(self.parent.component, self.key, self.edit_dialog.value)

        logger.info(f'Updated {self.key} to {self.edit_dialog.value}')

        if self.parent is not None:
            self.parent.ui_content.refresh()
        self.close()
