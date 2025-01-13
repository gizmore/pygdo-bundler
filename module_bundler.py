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
        self._priority = 200

    def gdo_module_config(self) -> list[GDT]:
        return [
        ]

    def gdo_load_scripts(self, page: 'GDT_Page'):
        self.minify_js(page)
        self.minify_css(page)

    def minify_js(self, page: 'GDT_Page'):
        internal = []
        external = []
        for file_name in page._js:
            if file_name.startswith('/'):
                internal.append(file_name)
            else:
                external.append(file_name)
        minified = JSMinifier(internal).execute()
        external.append("/" + Strings.substr_from(minified, Application.file_path()))
        page._js = external

    def minify_css(self, page: 'GDT_Page'):
        CSSMinifier(page._css).execute()
