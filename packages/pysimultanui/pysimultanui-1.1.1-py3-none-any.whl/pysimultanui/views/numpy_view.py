import numpy as np
import pandas as pd
from typing import Type
from nicegui import Client, app, ui, events
from .type_view import TypeView
from .type_view_manager import TypeViewManager

# from .detail_views import show_detail
from .. import user_manager
from ..core.edit_dialog import ContentEditDialog

from SIMULTAN.Data.MultiValues import (SimMultiValueField3D, SimMultiValueField3DParameterSource, SimMultiValueBigTable,
                                       SimMultiValueBigTableHeader, SimMultiValueBigTableParameterSource)

from PySimultan2.multi_values import simultan_multi_value_field_3d_to_numpy


class NDArrayDetailView(object):

    def __init__(self, *args, **kwargs) -> None:
        self.component: SimMultiValueField3D = kwargs.get('component')
        self.parent = kwargs.get('parent')
        self.array = None
        self.dim_slider = None
        self.table = None

    def ui_content(self, *args, **kwargs):

        from .detail_views import show_detail

        with ui.row().classes('w-full'):
            ui.input(label='Name',
                     value=self.component.Name).classes('w-full').bind_value(self.component, 'Name')
        with ui.row().classes('w-full'):
            ui.label('ID:').classes('w-full')
            with ui.row():
                with ui.row():
                    ui.label(f'{self.component.Id.GlobalId.ToString()}')
                with ui.row():
                    ui.label(f'{self.component.Id.LocalId}')

        self.array = simultan_multi_value_field_3d_to_numpy(self.component)

        with ui.row().classes('w-full'):
            with ui.column():
                ui.label('Shape:')
                ui.label(f'{self.array.shape}')

        ui.separator()

        self.table_ui_content()

        with ui.card().classes('w-full h-full'):
            ui.label('Dimension to display:')
            self.dim_slider = ui.slider(min=0, max=self.array.shape[0] - 1,
                                        step=1,
                                        value=0,
                                        on_change=self.table_ui_content.refresh)
            ui.input(value='0').bind_value(self.dim_slider,
                                           'value',
                                           forward=lambda x: int(x),
                                           backward=lambda x: str(x))

    @ui.refreshable
    def table_ui_content(self):

        if self.array.shape.__len__() > 2:
            disp_array = self.array[int(self.dim_slider.value if self.dim_slider is not None else 0), :, :]
        else:
            disp_array = self.array

        self.table = ui.table.from_pandas(pd.DataFrame(disp_array),
                                          ).classes('w-full h-full')
        with self.table.add_slot('top-left'):
            def toggle() -> None:
                self.table.toggle_fullscreen()
                button.props('icon=fullscreen_exit' if self.table.is_fullscreen else 'icon=fullscreen')

            button = ui.button('Toggle fullscreen', icon='fullscreen', on_click=toggle).props('flat')


class NDArrayView(TypeView):

    detail_view = NDArrayDetailView

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.content = kwargs.get('content', None)

    @ui.refreshable
    def ui_content(self):
        from .detail_views import show_detail
        with ui.card().classes(f"{self.colors['item']} w-full h-full") as self.card:
            self.card.on('click', lambda e: show_detail(value=self.component,
                                                        parent=self))
            with ui.row().classes('bg-stone-100 w-full') as self.row:
                self.row.on('click', lambda e: show_detail(value=self.component,
                                                           parent=self))
                self.checkbox = ui.checkbox(on_change=self.select)
                ui.label(f'{self.component.Id}')
                ui.label(f'{self.component.Name}')


class NDArrayManager(TypeViewManager):

    cls: np.ndarray = np.ndarray
    item_view_cls: Type[TypeView] = NDArrayView
    item_view_name = 'ND Arrays'

    def update_items(self) -> list[SimMultiValueField3D]:
        if self.data_model is None:
            return []
        return [x for x in self.data_model.value_fields if type(x) == SimMultiValueField3D]

    def button_create_ui_content(self):
        ui.button('Create new ND-Array', on_click=self.create_new_item, icon='add')

    @ui.refreshable
    def add_item_to_view(self,
                         item: any,
                         raw_val=None):

        if isinstance(item, SimMultiValueField3D):
            val_source = item
        elif isinstance(item, np.ndarray):
            val_source: SimMultiValueField3D = raw_val.ValueSource.ValueField

        if self.items_ui_element is None:
            return

        if val_source not in self.items:
            self.items.append(val_source)
        item_view = self.item_views.get(str(val_source.Id), None)

        if item_view is None:
            item_view = self.item_view_cls(component=val_source,
                                           parent=self)
            self.item_views[str(val_source.Id)] = item_view
            with self.items_ui_element:
                item_view.ui_content()
        else:
            if item_view.card.parent_slot.parent.parent_slot.parent is not self.items_ui_element:
                with self.items_ui_element:
                    item_view.ui_content()
        return item_view
