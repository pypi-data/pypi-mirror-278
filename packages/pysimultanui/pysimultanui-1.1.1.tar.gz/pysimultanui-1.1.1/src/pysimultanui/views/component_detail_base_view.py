from nicegui import ui, events, app

from .. import user_manager
from ..core.geo_associations import GeoEditDialog

from PySimultan2.simultan_object import SimultanObject


class ComponentDetailBaseView(object):

    def __init__(self, *args, **kwargs):
        self.component: SimultanObject = kwargs.get('component')
        self.parent = kwargs.get('parent')
        self.card = None
        self.row = None

        self.table = None
        self.association_table = None

    @property
    def user(self):
        return user_manager[app.storage.user['username']]

    @ui.refreshable
    def ui_content(self, *args, **kwargs):
        # with ui.card().classes('w-full h-full'):
        with ui.row().classes('w-full'):
            ui.input(label='Name', value=self.component.name).bind_value(self.component, 'name').classes('w-full').style('font-size: 1.25em;')
            ui.button('Create Copy', icon='file_copy', on_click=self.create_copy)
        with ui.row():
            ui.label('Global ID: ')
            ui.label(f'{self.component.id.GlobalId.ToString()}')
            ui.label('Local ID: ')
            ui.label(f'{self.component.id.LocalId}')
        self.ui_content_associate_geometry()

    def ui_content_associate_geometry(self):
        with ui.expansion(icon='format_list_bulleted',
                          text=f'Associated Geometry').classes('w-full') as exp:

            columns = [{'name': 'id', 'label': 'ID', 'field': 'id', 'sortable': True},
                       {'name': 'name', 'label': 'Name', 'field': 'name', 'sortable': True},
                       {'name': 'type', 'label': 'Type', 'field': 'type', 'sortable': True},
                       {'name': 'actions', 'label': 'Actions', 'field': 'actions', 'sortable': False}]

            rows = [{'id': x.id,
                     'name': x.name,
                     'type': x.__class__.__name__}
                    for x in self.component.associated_geometry]

            self.association_table = ui.table(columns=columns,
                                              rows=rows,
                                              title='Associated Geometry',
                                              pagination={'rowsPerPage': 5, 'sortBy': 'id', 'page': 1},
                                              row_key='id').classes('w-full h-full bordered')

            self.association_table.add_slot('body-cell-actions', r'''
                                                        <q-td key="actions" :props="props">
                                                            <q-btn size="sm" color="blue" round dense
                                                                @click="$parent.$emit('show_detail', props)"
                                                                icon="launch" />
                                                            <q-btn size="sm" color="negative" round dense
                                                                @click="$parent.$emit('delete_association', props)"
                                                                icon="delete" />
                                                        </q-td>
                                                    ''')

            self.association_table.on('show_detail', self.show_geo_detail)
            self.association_table.on('delete_association', self.delete_association)

            ui.button('Add Association', on_click=self.edit_association)

    def refresh(self):
        self.ui_content.refresh()

    def show_geo_detail(self, e: events.GenericEventArguments):
        from .detail_views import show_detail
        instance = next((x for x in self.component.associated_geometry if x.id == e.args['row'].get('id')), None)._geometry_model
        show_detail(value=instance)

    def edit_association(self):
        edit_dialog = GeoEditDialog(component=self.component,
                                    parent=self)
        edit_dialog.create_edit_dialog()

    def delete_association(self, e: events.GenericEventArguments):
        instance = next((x for x in self.component.associated_geometry if x.id == e.args['row'].get('id')), None)
        instance.disassociate(self.component)
        ui.notify(f'Removed associated {instance.name} from {self.component.name}')
        self.ui_content.refresh()

    def create_copy(self, e: events.GenericEventArguments):
        new_instance = self.component.copy()
        self.user.project_manager.mapped_data.append(new_instance)
        self.user.grid_view.add_item_to_view(new_instance)
        ui.notify(f'Created copy {new_instance.name} {new_instance.id} of {self.component.name}, {self.component.id}')
