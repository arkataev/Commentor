from string import Template
import os
import re


class Renderer:

    def __init__(self):
        self.template_folder = os.path.abspath('static')

    def render(self, fname, **kwargs):
        extends = self._extends(fname)
        if extends:
            template = self._get_template(self._read_template(extends))
            block = self._get_block(self._read_template(fname))
            html = template.substitute(block)
        else: html = self._read_template(fname)
        return self._map_vars(html, **kwargs)

    def _map_vars(self, html, **kwargs):
        template = self._get_template(html)
        return template.substitute(**kwargs)

    def _get_template(self, html:str) -> Template:
        return Template(html)

    def _read_template(self, fname:str):
        path = self._template_path(fname)
        with open(path) as f:
            html = f.read()
            return html

    def _template_path(self, fname):
        path = os.path.join(self.template_folder, fname)
        if not os.path.exists(path):
            raise FileNotFoundError('File {} not found at {}'.format(fname, path))
        return path

    def _extends(self, fname:str) -> str or bool:
        regex = re.compile(r"(?P<command>@[a-z]+)\((?P<value>.*)\)")
        path = self._template_path(fname)
        with open(path) as f:
            params = regex.search(f.readline())
            return params.group(2) if params else False

    def _get_block(self, html):
        regex = re.compile(r"@block\(\'(?P<name>[^\)]+)\'\)(?P<content>.*)@endblock", re.DOTALL)
        res = regex.search(html)
        return res.groupdict()

