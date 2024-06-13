
from fluke.sites import site
from fluke.views import BaseAdminPlugin, CommAdminView

BUILDIN_STYLES = {
    'default': 'fluke/includes/sitemenu_default.html',
    'accordion': 'fluke/includes/sitemenu_accordion.html',
}


class SiteMenuStylePlugin(BaseAdminPlugin):

    menu_style = None

    def init_request(self, *args, **kwargs):
        return bool(self.menu_style) and self.menu_style in BUILDIN_STYLES

    def get_context(self, context):
        context['menu_template'] = BUILDIN_STYLES[self.menu_style]
        return context

site.register_plugin(SiteMenuStylePlugin, CommAdminView)
