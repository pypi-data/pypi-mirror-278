from contextlib import contextmanager
from .menue import menu
from nicegui import app, ui, context
from .. import user_manager

from ..__about__ import __version__
from . import home
from . import project

from .. import core


@contextmanager
def frame(navtitle: str):

    """Custom page frame to share the same styling and behavior across all pages"""
    # ui.colors(primary='#da291c', secondary='#941c13', accent='#941c13', positive='#53B689')
    with ui.header().classes('justify-between'):

        user = user_manager.users[app.storage.user['username']]

        # ui.image('web_ui/src/static_files/A1_Digital_identifier_pos_RGB.png').classes('w-32')

        with ui.column():
            ui.label('PY Simultan').classes('font-bold text-white text-xl')
            ui.button(on_click=lambda: (user_manager.users[app.storage.user['username']].logout(),
                                        app.storage.user.clear(),
                                        ui.navigate.to('/login')), icon='logout')

        with ui.column():
            ui.label(f'Hello {user.name}').classes('text-white text-xl')
            ui.label(f'Version {__version__}')

        # with ui.expansion('Menu', icon='select'):
        with ui.column():
            with ui.tabs() as tabs:
                # ui.button('Mapped Classes', icon='checklist_rtl', on_click=lambda: left_drawer.toggle())
                ui.tab('Home', icon='home')
                ui.tab('Project', icon='edit')
                ui.tab('Logs', icon='format_list_bulleted')

                # ui.button(on_click=lambda: (app.storage.user.clear(),
                #                             ui.open('/login')),
                #           icon='logout').props('outline round').classes('text-black')
                #


                # with ui.button(icon='menu'):
                #     with ui.menu() as menu:
                #         ui.menu_item('Logout',
                #                      icon='logout',
                #                      on_click=lambda: (app.storage.user.clear(), ui.open('/login')))

                # ui.space()
                # if app.storage.user.get('username', False):
                #     ui.label(f'{app.storage.user["username"]}').classes('mr-auto text-2xl')

    # with ui.left_drawer(bordered=True,
    #                     top_corner=False,
    #                     elevated=True,
    #                     fixed=True,
    #                     value=False).classes('bg-blue-100') as left_drawer:
    #     user.navigation_drawer = left_drawer

    # with ui.splitter() as splitter:
    #     with splitter.after:
    #         with ui.right_drawer(bordered=True,
    #                              top_corner=False,
    #                              elevated=True,
    #                              fixed=True,
    #                              value=False).classes('w-full h-full') as detail_view:
    #             core.detail_view = detail_view

    with ui.tab_panels(tabs, value='Home').classes('w-full h-full'):
        with ui.tab_panel('Project').classes('w-full h-full') as project_full_tab:
            with ui.splitter(value=60, limits=(10, 90)).classes('w-full h-full') as splitter:
                with splitter.before as project_tab:
                    context.client.content.classes('h-[95vh]')
                    user.project_tab = project_tab
                with splitter.after:
                    user.detail_view = ui.row().classes('w-full h-full')

        user.home_tab = ui.tab_panel('Home').classes('w-full h-full')

        with ui.tab_panel('Logs').classes('w-full h-full'):
            with ui.card().classes('w-full h-full') as logs_tab:
                user.log_tab = logs_tab

    with user.home_tab:
        home.content()
