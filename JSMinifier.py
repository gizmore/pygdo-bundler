import subprocess

from gdo.base.Application import Application
from gdo.base.Logger import Logger
from gdo.base.Util import Files, dump, Strings
from gdo.core.GDT_MD5 import GDT_MD5


class JSMinifier:

    _files: list[str]

    def __init__(self, files: list[str]):
        self._files = files

    def output_path(self) -> str:
        return Application.file_path(f'assets/{self.output_hash()}.js')

    def output_hash(self) -> str:
        return GDT_MD5.hash_for_str("|".join(self._files))

    def execute(self):
        internal = []
        external = []
        for file_name in self._files:
            if file_name.startswith('//'):
                external.append(file_name)
            elif file_name.startswith('/'):
                internal.append(file_name)
            else:
                external.append(file_name)
        out_path = self.output_path()
        if Files.exists(out_path):
            return out_path
        out_content = ''
        for file_name in self._files:
            try:
                path = Application.file_path(file_name.strip('/'))
                path = Strings.substr_to(path, '?')
                out_content += self.minify(path)
                out_content += ";\n"
            except Exception as ex:
                Logger.exception(ex)
        Files.put_contents(out_path, out_content)
        external.append("/" + Strings.substr_from(out_path, Application.file_path()))
        Application.get_page()._js = external

    def minify(self, path: str) -> str:
        bin = Application.file_path('gdo/bundler/node_modules/terser/bin/terser')
        args = [bin, '--screw-ie8', '-m', '-c', 'drop_console=true', '--', path]
        process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8'
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"UglifyJS failed: {stderr}")
        return stdout
