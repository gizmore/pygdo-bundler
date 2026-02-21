from gdo.base.Application import Application
from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.base.Util import Files, Strings
from gdo.bundler.CSSMinifier import CSSMinifier
from gdo.bundler.HTMLBeautifier import HTMLBeautifier
from gdo.bundler.HTMLMinifier import HTMLMinifier
from gdo.bundler.JSMinifier import JSMinifier
from gdo.core.GDT_Enum import GDT_Enum
from gdo.core.GDT_String import GDT_String
from gdo.ui.GDT_Page import GDT_Page


class module_bundler(GDO_Module):

    def __init__(self):
        super().__init__()
        self._priority = 2088

    def gdo_module_config(self) -> list[GDT]:
        return [
            GDT_Enum('html_mode').choices({'minify': 'Minify', 'beautify': 'Beautify'}).initial('beautify'),
        ]

    def cfg_html_mode(self) -> str:
        return self.get_config_val('html_mode')

    def gdo_subscribe_events(self):
        if self.cfg_html_mode():
            Application.EVENTS.subscribe('render_html', self.render_html_event)

    async def render_html_event(self, s: GDT_String):
        mode = self.cfg_html_mode()
        if mode == 'minify':
            s.val(HTMLMinifier.minify(s.get_val()))
        elif mode == 'beautify':
            s.val(HTMLBeautifier.beautify(s.get_val()))

    def gdo_init(self):
        Files.create_dir(Application.file_path(f'assets/'))

    def gdo_load_scripts(self, page: 'GDT_Page'):
        JSMinifier(GDT_Page._js).execute()
        CSSMinifier(GDT_Page._css).execute()
