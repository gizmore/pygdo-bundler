from gdo.base.Application import Application
from gdo.base.GDO_Module import GDO_Module
from gdo.base.GDT import GDT
from gdo.base.Util import Files, Strings
from gdo.bundler.CSSMinifier import CSSMinifier
from gdo.bundler.JSMinifier import JSMinifier
from gdo.ui.GDT_Page import GDT_Page


class module_bundler(GDO_Module):

    def __init__(self):
        super().__init__()
        self._priority = 2088

    def gdo_module_config(self) -> list[GDT]:
        return [
        ]

    def gdo_install(self):
        Files.create_dir(Application.file_path(f'assets/{GDO_Module.CORE_REV}/'))

    def gdo_load_scripts(self, page: 'GDT_Page'):
        JSMinifier(GDT_Page._js).execute()
        CSSMinifier(GDT_Page._css).execute()
