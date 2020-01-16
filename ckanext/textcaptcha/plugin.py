import requests
import hashlib
import logging

from builtins import str

import ckan.plugins as p
import ckan.logic as logic
import ckan.plugins.toolkit as tk
import ckan.logic.auth.create as create_auth
import ckan.model as model

from ckan.common import _

from ckanext.textcaptcha.helpers import get_helpers

if tk.check_ckan_version("2.9"):
    config = tk.config
else:
    from pylons import config

session = model.Session
log = logging.getLogger(__name__)


class TextCaptchaPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)
    
    # IAuthFunctions
    def get_auth_functions(self):
        """Redeclare auth functions."""
        return {
            "user_create": textcaptcha_user_create
        }

    # ITemplateHelpers
    def get_helpers(self):
        return get_helpers()

    # IConfigurer
    def update_config(self, config):
        tk.add_template_directory(config, "templates")
        tk.add_resource("public", "ckanext-textcaptcha")
        tk.add_public_directory(config, "public")


@logic.auth_allow_anonymous_access
def textcaptcha_user_create(context, data_dict=None):
    """Create user."""
    if data_dict:
        a = str(data_dict.get("textcaptcha"))

        a = (hashlib.md5(a.lower().encode('utf-8')).hexdigest()
            if isinstance(a, str) else "  not valid  ")

        v = data_dict.get("textcaptcha_opt")
        log.warn(a)
        log.warn(v)
        if not all([a, v, a in v]):
            raise tk.ValidationError(
                {"spam_prevention": [_("Wrong answer")]}
            )
    return create_auth.user_create(context, data_dict)
