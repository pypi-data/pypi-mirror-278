from nicegui import ui
import logging
from ..type_view import TypeView
from nicegui import ui, app, events

from ... import user_manager
# from ... import core

from ..component_detail_base_view import ComponentDetailBaseView
from ...core.edit_dialog import ContentEditDialog
from PySimultan2.simultan_object import SimultanObject
from PySimultan2.default_types import ComponentList

from ..parameter_view import ParameterView
from ..mapped_cls.mapped_cls_view import ContentItemView
from ...core.geo_associations import GeoEditDialog

from SIMULTAN.Data import SimId
from System import Guid

logger = logging.getLogger('py_simultan_ui')


class ListItemView(object):

    def __init__(self, *args, **kwargs):
        self.component: SimultanObject = kwargs.get('component')
        self.parent = kwargs.get('parent')
        self.item_no = kwargs.get('item_no')
        self.first = kwargs.get('first', False)
        self.last = kwargs.get('last', False)

    @property
    def view_manager(self):
        return self.parent.view_manager

    @ui.refreshable
    def ui_content(self):

        from ..detail_views import show_detail

        with ui.item().classes('w-full h-full'):
            with ui.item_section():
                ui.label(f'Item {self.item_no}:')
            if hasattr(self.component, '__ui_element__') and self.component.__ui_element__ is None:
                if self.component.__class__ not in self.view_manager.cls_views:
                    self.view_manager.create_mapped_cls_view_manager(taxonomy=self.component.__class__._taxonomy)
                self.view_manager.cls_views[self.component.__class__]['item_view_manager'].add_item_to_view(
                    self.component
                )
            # with ui.item_section():
            #     ui.label(f'{self.component.name}').on('click', self.component.__ui_element__.show_details)
                # ui.link(self.component.name, self.component.__ui_element__.card)

            with ui.item_section():
                ui.label(f'{self.component.name}')

            with ui.item_section():
                ui.button(on_click=lambda e: show_detail(self.component),
                          icon='launch').classes('q-ml-auto')

            with ui.item_section():
                with ui.row():
                    ui.label(f'{self.component.Id.GlobalId.ToString()}')
                with ui.row():
                    ui.label(f'{self.component.Id.LocalId}')

            with ui.item_section():
                button = ui.button(on_click=self.edit,
                                   icon='edit').classes('q-ml-auto')
                button.item = self.component
                button.item_no = self.item_no
            with ui.item_section():
                with ui.row():
                    if not self.first:
                        button = ui.button(on_click=self.move_up,
                                           icon='keyboard_arrow_up').classes('q-ml-auto')
                        button.item = self.component
                        button.item_no = self.item_no
                    else:
                        ui.label('')
                with ui.row():
                    if not self.last:
                        button = ui.button(on_click=self.move_down,
                                           icon='keyboard_arrow_down').classes('q-ml-auto')
                        button.item = self.component
                        button.item_no = self.item_no
                    else:
                        ui.label('')

            with ui.item_section():
                button = ui.button(on_click=self.remove,
                                   icon='delete').classes('q-ml-auto')
                button.item = self.component
                button.item_no = self.item_no

    def edit(self, event):
        ui.notification('Edit not implemented yet', type='negative')

    def remove(self, event):
        self.parent.component.discard(event.sender.item)
        self.parent.list_content.refresh()

    def move_up(self, event):
        if self.item_no > 0:
            self.parent.component.move_item(event.sender.item, event.sender.item_no - 1)
        self.parent.list_content.refresh()

    def move_down(self, event):
        if self.item_no < len(self.parent.component) - 1:
            self.parent.component.move_item(event.sender.item, event.sender.item_no + 1)
        self.parent.list_content.refresh()


class ListView(object):

    def __init__(self, *args, **kwargs):
        self.component: ComponentList = kwargs.get('component')
        self.parent = kwargs.get('parent')
        self.card = None

        self.content_item_views: dict[str: ContentItemView] = {}

    @property
    def view_manager(self):
        return self.parent.view_manager

    @ui.refreshable
    def list_content(self):
        with ui.list().classes('w-full h-full'):

            for i, item in enumerate(self.component):

                if self.content_item_views.get(i, None) is None or self.content_item_views[i].component != item:
                    self.content_item_views[i] = ListItemView(component=item,
                                                              parent=self,
                                                              item_no=i,
                                                              first=i == 0,
                                                              last=i == len(self.component) - 1)
                self.content_item_views[i].ui_content()
                ui.separator()

        try:
            ui.button(f'Add new item to {self.component.name}',
                      on_click=self.parent.add_new_item, icon='add').classes('q-ml-auto')
        except Exception as e:
            logger.error(f'Error adding new item: {e}')

    @ui.refreshable
    def ui_content(self):
        with ui.expansion(icon='format_list_bulleted',
                          text=f'Content ({len(self.component)})',
                          value=True
                          ).classes('w-full h-full').bind_text_from(self,
                                                                    'data',
                                                                    lambda x: f'Content ({len(self.component)})'
                                                                    ) as self.card:
            self.list_content()


class ListDetailView(ComponentDetailBaseView):

    columns = [
        {'name': 'item_id',
         'label': 'Item ID',
         'field': 'item_id',
         'align': 'left',
         'sortable': True},
        {'name': 'name',
         'label': 'Name',
         'field': 'name',
         'sortable': True},
        {'name': 'component_id',
         'label': 'Component ID',
         'field': 'component_id',
         'sortable': True},
        {'name': 'item_type',
         'label': 'Item Type',
         'field': 'item_type',
         'sortable': True},
        {'name': 'type',
         'label': 'Type',
         'field': 'type',
         'sortable': True},
    ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    @property
    def items(self) -> list[dict]:
        items = [{}] * len(self.component.data)

        for i, item in enumerate(self.component.data):
            if item._wrapped_obj in self.component.components:
                c_type = 'Subcomponent'
            elif item._wrapped_obj in self.component.ref_components:
                c_type = 'Reference'
            else:
                c_type = 'Undef'

            items[i] = {'item_id': str(i),
                        'name': item.name,
                        'component_id': f'{item.id.GlobalId}_{item.id.LocalId}',
                        'item_type': f'{item.__class__.__name__}',
                        'type': c_type
                        }
        return items

    @ui.refreshable
    def ui_content(self):
        super().ui_content()

        with ui.table(columns=self.columns,
                      rows=self.items,
                      row_key='item_id').classes('w-full bordered') as self.table:

            # self.table.add_slot('header', r'''
            #         <q-tr :props="props">
            #             <q-th auto-width />
            #             <q-th v-for="col in props.cols" :key="col.name" :props="props">
            #                 {{ col.label }}
            #             </q-th>
            #         </q-tr>
            #     ''')

            # Modify the table body slot for delete functionality
            self.table.add_slot('body', r'''
                    <q-tr :props="props">
                        <q-td v-for="col in props.cols" :key="col.name" :props="props">
                            {{ col.value }}
                        </q-td>
                        <q-td auto-width>
                            <q-btn size="sm" color="blue" round dense
                                   @click="$parent.$emit('detail', props)"
                                   icon="launch" />
                            <q-btn size="sm" color="positive" round dense
                                   @click="$parent.$emit('up', props)"
                                   icon="keyboard_arrow_up" />
                            <q-btn size="sm" color="positive" round dense
                                   @click="$parent.$emit('down', props)"
                                   icon="keyboard_arrow_down" />
                            <q-btn size="sm" color="negative" round dense
                                   @click="$parent.$emit('delete', props)"
                                   icon="delete" />
                        </q-td>
                    </q-tr>
                ''')

            # self.table.add_slot('body', r'''
            #     <q-td :props="props">
            #         <q-btn @click="$parent.$emit('delete', props)" icon="delete" flat dense color='green'/>
            #     </q-td>
            # ''')

            self.table.on('delete', self.remove)
            self.table.on('up', self.move_up)
            self.table.on('down', self.move_down)
            self.table.on('detail', self.show_details)

            ui.button(f'Add new item to {self.component.name}',
                      on_click=self.add_new_item, icon='add').classes('q-ml-auto')

        ui.button('Add Item', on_click=self.add_new_item, icon='add')

    def get_instance_row(self, props):
        return self.component[int(props.args['row'].get('item_id'))]

    def remove(self, props):
        instance = self.get_instance_row(props)

        other_refs = [ref.Target for ref in instance._wrapped_obj.ReferencedBy
                      if ref.Target is not self.component._wrapped_obj]

        if other_refs:
            ui.notify(f"Cannot remove {instance.name} because it is referenced by "
                      f'{[(ref.Name, ref.Id) for ref in other_refs]}',
                      type='negative',
                      close_button='OK')
            return

        self.component.discard(instance)
        self.ui_content.refresh()

    def move_up(self, props):
        instance = self.get_instance_row(props)
        item_no = int(props.args['row'].get('item_id'))
        if item_no > 0:
            self.component.move_item(instance, item_no - 1)
        self.ui_content.refresh()

    def move_down(self, props):
        instance = self.get_instance_row(props)
        item_no = int(props.args['row'].get('item_id'))
        if item_no < len(self.parent.component) - 1:
            self.component.move_item(instance, item_no + 1)
        self.ui_content.refresh()

    def show_details(self, props):
        from ..detail_views import show_detail
        instance = self.get_instance_row(props)
        show_detail(value=instance)

    def add_new_item(self, event):

        component = self.component
        edit_dialog = ContentEditDialog(component=None,
                                        parent=self,
                                        content=None,
                                        options=['Component'])

        def save(*args, **kwargs):
            if isinstance(edit_dialog.edit_dialog.value, list):
                component.extend(edit_dialog.edit_dialog.value)
            else:
                component.append(edit_dialog.edit_dialog.value)
            edit_dialog.close()
            self.ui_content.refresh()

        edit_dialog.save = save
        edit_dialog.create_edit_dialog()

    def refresh(self):
        self.ui_content()


class ComponentListView(TypeView):

    detail_view = ListDetailView

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def view_manager(self):
        return self.parent.view_manager

    @ui.refreshable
    def ui_content(self):
        from ..detail_views import show_detail

        with ui.card().classes(f"{self.colors['item']} w-full h-full") as self.card:
            self.card.on('click', lambda e: show_detail(self.component))
            with ui.row().classes('bg-stone-100 w-full') as self.row:
                self.row.on('click', lambda e: show_detail(self.component))
                self.checkbox = ui.checkbox()
                ui.input(label='Name', value=self.component.name).bind_value(self.component, 'name')
                ui.label(f'{str(self.component.id)}')

            # self.content_view.ui_content()

    def show_details(self, *args, **kwargs):
        self.detail_view(component=self.component,
                         parent=self).ui_content()

    def add_new_item(self, event):

        component = self.component
        edit_dialog = ContentEditDialog(component=None,
                                        parent=self,
                                        content=None,
                                        options=['Component'])

        def save(self, *args, **kwargs):
            if isinstance(edit_dialog.edit_dialog.value, list):
                component.extend(edit_dialog.edit_dialog.value)
            else:
                component.append(edit_dialog.edit_dialog.value)
            component.__ui_element__.content_view.list_content.refresh()
            edit_dialog.close()

        edit_dialog.save = save
        edit_dialog.create_edit_dialog()
