from string import Template
import os
import re

STATIC_FOLDER  = os.path.abspath('static')
TEMPLATE_FOLDER = os.path.abspath('static/templates')

class Renderer:

    def __init__(self):
        self.template_folder = STATIC_FOLDER
        # self.static_folder = os.path.join('','static')

    def render(self, fname, **kwargs):
        extends = self._extends(fname)
        if extends:
            template = self._get_template(self._read_template(extends))
            block = self._get_block(self._read_template(fname))
            html = template.substitute(block)
        else: html = self._read_template(fname)
        if 'embed_html' in kwargs: kwargs['embed'] = self._embed_html(kwargs)
        return self._map_vars(html, **kwargs)

    def _embed_html(self, data):
        emb_html = data.pop('embed_html')
        mapped_html = self._map_vars(emb_html, **data.pop('vars'))
        return mapped_html

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

