import os
from pathlib import Path
from typing import Optional
from nicegui import app as ng_app, ui, Client
from .app.theme import frame

from .app.auth import AuthMiddleware
from .app import login
from .app import project

unrestricted_page_routes = {'/login'}

ng_app.add_middleware(AuthMiddleware)
# ui.add_head_html("<style>" + open(Path(__file__).parent / "static_files" / "styles.css").read() + "</style>")


@ui.page('/')
def index_page(client: Client) -> None:
    frame('Home')
    login.content()
    # with frame('Home'):
    #     home.content()


@ui.page('/login')
def index_page() -> None:
    # frame('Home')
    # with frame('Home'):
    #     pass
    login.content()


@ui.page('/project')
def index_page(client: Client) -> None:
    # frame('Home')
    # with frame('Home'):
    #     pass
    frame('Project')


# app.on_shutdown(handle_shutdown)
def run_ui():
    ui.run(storage_secret=os.environ.get('STORAGE_SECRET', 'my_secret'),
           title='Py Simultan',
           dark=False,
           reload=True)


if __name__ == '__main__':
    run_ui()
