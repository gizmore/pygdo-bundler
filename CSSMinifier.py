import rcssmin

from gdo.base.Application import Application
from gdo.base.DBLock import DBLock
from gdo.base.Exceptions import GDOException
from gdo.base.GDO_Module import GDO_Module
from gdo.base.Util import Files, Strings
from gdo.core.GDT_MD5 import GDT_MD5
from gdo.ui.GDT_Page import GDT_Page


class CSSMinifier:

    _files: list[str]

    def __init__(self, files: list[str]):
        self._files = files

    def get_output_hash(self) -> str:
        return GDT_MD5.hash_for_str("|".join(self._files))

    def get_output_path(self):
        return Application.file_path(f'assets/{GDO_Module.cache_key()}/{self.get_output_hash()}.css')

    def execute(self):
        out_path = self.get_output_path()
        out_content = ''
        external, internal = [], []
        for file_name in self._files:
            (external if file_name.startswith('//') or not file_name.startswith('/') else internal).append(file_name)
        if not Files.is_file(out_path):
            try:
                with DBLock('css_minify', 1):
                    for file_name in internal:
                        out_content += self.minify(file_name)
                    Files.put_contents(out_path, out_content)
            except GDOException as ex:
                pass
        external.append('/'+Strings.substr_from(out_path, Application.file_path()))
        GDT_Page._css = external

    def minify(self, file_name: str):
        file_name = Strings.substr_to(file_name, '?', file_name).lstrip('/')
        path = Application.file_path(file_name)
        return rcssmin.cssmin(Files.get_contents(path))
