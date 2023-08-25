import logging

import ckan.plugins as p
import ckan.plugins.toolkit as tk

log = logging.getLogger(__name__)


@tk.blanket.helpers
@tk.blanket.auth_functions
class TextCaptchaPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)

    # IConfigurer
    def update_config(self, config):
        tk.add_template_directory(config, "templates")
        tk.add_resource("public", "ckanext-textcaptcha")
        tk.add_public_directory(config, "public")
