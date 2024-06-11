from jinja2 import Environment, FileSystemLoader, PackageLoader, select_autoescape
from .settings import settings

template_env = Environment(
    loader=PackageLoader(settings.template_theme, 'templates'),
    #loader=FileSystemLoader('templates'),

    autoescape=select_autoescape(['html', 'xml'])
)
