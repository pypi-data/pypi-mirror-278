from nicegui import events, ui, app

from typing import Optional
from .. import user_manager
from .detail_views import show_detail

from SIMULTAN.Data import SimId
from PySimultan2.simultan_object import SimultanObject
from System import Guid


class GridView(object):

    columns = [
        {'headerName': 'Name',
         'field': 'name',
         'editable': True,
         'sortable': True,
         'filter': 'agTextColumnFilter',
         'floatingFilter': True,
         'checkboxSelection': True},
        {'headerName': 'ID',
         'field': 'id',
         'editable': False,
         'sortable': True,
         'filter': 'agTextColumnFilter',
         'floatingFilter': True},
        {'headerName': 'Mapped Class',
         'field': 'taxonomy',
         'editable': False,
         'sortable': True,
         'filter': 'agTextColumnFilter',
         'floatingFilter': True},
    ]

    def __init__(self, *args, **kwargs):

        self._data_model = None
        self.table: Optional[ui.aggrid] = None

        self.create_type_select: Optional[ui.select] = None
        self.create_type: Optional[str] = None             # type of object to create

    @property
    async def selected_instances(self):
        rows = await self.table.get_selected_rows()
        return [
            self.mapper.get_mapped_class(row['taxonomy'])._cls_instances_dict.get(SimId(Guid(row['id'].split('_')[0]),
                                                                                        int(row['id'].split('_')[1])),
                                                                                  None) for row in rows]

    @property
    def data_model(self):
        return self._data_model

    @data_model.setter
    def data_model(self, value):
        self._data_model = value
        self.ui_content.refresh()

    @property
    def mapper(self):
        return self.user.mapper

    @property
    def user(self):
        return user_manager[app.storage.user['username']]

    @property
    def items(self) -> list[dict[str: str,
                                 str: str,
                                 str: str]]:
        items = []

        for taxonomy, cls in self.mapper.mapped_classes.items():
            if hasattr(cls, 'cls_instances'):
                for instance in cls.cls_instances:
                    items.append({'name': instance.name,
                                  'id': f'{instance.id.GlobalId}_{instance.id.LocalId}',
                                  'taxonomy': taxonomy})

        return items

    @ui.refreshable
    def ui_content(self):

        self.table = ui.aggrid({
            'columnDefs': self.columns,
            'rowData': self.items,
            'auto_size_columns': True,
            'rowSelection': 'multiple',
            'pagination': True,
            'paginationPageSize': 25,
            'paginationPageSizeSelector': [10, 25, 50, 100, 150, 200],
            'enableFilter': True,
        },
            auto_size_columns=True).on('cellClicked', lambda e: self.show_detail(e))

        # self.table.add_slot('body-cell-actions', r'''
        #                                                         <q-td key="actions" :props="props">
        #                                                             <q-btn size="sm" color="blue" round dense
        #                                                                 @click="$parent.$emit('show_detail', props)"
        #                                                                 icon="launch" />
        #                                                             <q-btn size="sm" color="blue" round dense
        #                                                                 @click="$parent.$emit('create_copy', props)"
        #                                                                 icon="file_copy" />
        #                                                         </q-td>
        #                                                     ''')
        #
        # self.table.on('show_detail', lambda e: self.show_detail(e))
        # self.table.on('create_copy', lambda e: self.create_copy(e))

        self.table.classes('w-full h-full')
        self.ui_create_new_content()
        self.user.method_mapper.ui_content()

        ui.button(on_click=self.user.project_manager.refresh_all_items,
                  icon='update').props('fab color=accent')

    def ui_create_new_content(self):

        with ui.expansion(icon='add',
                          text='Create new').classes('w-full'):

            with ui.column().classes('w-full'):
                self.create_type_select = ui.select(options=[taxonomy for taxonomy in
                                                             self.user.mapper.mapped_classes.keys()],
                                                    value=list(self.user.mapper.mapped_classes.keys())[0]
                                                    if self.user.mapper.mapped_classes.keys() else None,
                                                    label='Mapped Class').classes('w-full').bind_value(self,
                                                                                                       'create_type')
            with ui.column():
                ui.button(icon='play_circle', on_click=self.create_new_item).classes('w-full')

    def create_new_item(self, e):

        if None in (self.data_model, self.create_type):
            ui.notify('No data model selected! Please load a data model first.')
            return

        cls = self.user.mapper.get_mapped_class(self.create_type)
        if cls is None:
            ui.notify(f'Could not find class for taxonomy {self.create_type}.')
            return
        new_item: SimultanObject = cls(data_model=self.data_model,
                                       object_mapper=self.mapper,
                                       )
        new_item.name = f'New {cls.__name__}_{new_item.id}'

        self.user.logger.info(f'Created new {cls.__name__}, ID {new_item.id}.')

        self.user.project_manager.mapped_data.append(new_item)

        self.data_model.save()
        self.add_item_to_view(new_item)
        self.mapper.get_mapped_class(self.create_type)._cls_instances_dict.get(new_item.id, None)

        show_detail(value=new_item)
        ui.notify(f'Created new {cls.__name__}, ID {new_item.id}.')

    def selected_rows(self):
        rows = self.table.get_selected_rows()
        if rows:
            for row in rows:
                ui.notify(f"{row['name']}, {row['age']}")
        else:
            ui.notify('No rows selected.')

    def show_detail(self, e):

        component_id = e.args['data']['id']
        sim_id = SimId(Guid(component_id.split('_')[0]), int(component_id.split('_')[1]))
        instance = self.mapper.get_mapped_class(e.args['data']['taxonomy'])._cls_instances_dict.get(sim_id, None)
        if instance is None:
            return
        show_detail(value=instance)

    def add_item_to_view(self, component: SimultanObject):
        self.ui_content.refresh()

#
#
#
# def rename(e: events.GenericEventArguments) -> None:
#     for row in rows:
#         if row["id"] == e.args["id"]:
#             row.update(e.args)
#     ui.notify(f"Table.rows is now: {table.rows}")
#
#
# def delete(e: events.GenericEventArguments) -> None:
#     rows[:] = [row for row in rows if row["id"] != e.args["id"]]
#     ui.notify(f"Delete {e.args['id']}")
#     table.update()
#
#
# def addrow() -> None:
#     newid = max(dx["id"] for dx in rows) + 1
#     rows.append({"id": newid, "name": "New guy", "age": 21})
#     ui.notify(f"Added new row with id {newid}")
#     table.update()
#
#
# table = ui.table(columns=columns, rows=rows, row_key="name").classes("w-72")
# table.add_slot(
#     "header",
#     r"""
#     <q-tr :props="props">
#         <q-th auto-width />
#         <q-th v-for="col in props.cols" :key="col.name" :props="props">
#             {{ col.label }}
#         </q-th>
#     </q-tr>
# """,
# )
# table.add_slot(
#     "body",
#     r"""
#     <q-tr :props="props">
#         <q-td auto-width >
#             <q-btn size="sm" color="warning" round dense icon="delete" :props="props"
#                 @click="() => $parent.$emit('delete', props.row)" >
#         </q-td>
#         <q-td key="name" :props="props">
#             {{ props.row.name }}
#             <q-popup-edit v-model="props.row.name" v-slot="scope"
#                 @update:model-value="() => $parent.$emit('rename', props.row)" >
#                 <q-input v-model="scope.value" dense autofocus counter @keyup.enter="scope.set" />
#             </q-popup-edit>
#         </q-td>
#         <q-td key="age" :props="props" class="w-8">
#             {{ props.row.age }}
#             <q-popup-edit v-model="props.row.age" v-slot="scope"
#                 @update:model-value="() => $parent.$emit('rename', props.row)" >
#                 <q-input v-model.number="scope.value" type="number" dense autofocus counter @keyup.enter="scope.set" />
#             </q-popup-edit>
#         </q-td>
#     </q-tr>
#     """,
# )
# table.add_slot(
#     "bottom-row",
#     r"""
#     <q-tr :props="props">
#         <q-td colspan="3" class="text-center">
#             <q-btn color="accent" icon="add" class="w-full" @click="() => $parent.$emit('addrow')"/>
#         </q-td>
#     </q-tr>
#     """,
# )
# table.on("rename", rename)
# table.on("delete", delete)
# table.on("addrow", addrow)
#
# ui.run()
