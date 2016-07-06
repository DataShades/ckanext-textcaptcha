import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.logic as logic
import ckan.plugins.toolkit as tk
import ckan.logic.auth.create as create_auth
from ckan.common import _
import ckan.model as model
from pylons import config

import requests
import hashlib
import logging
session = model.Session
log = logging.getLogger(__name__)


class TextCaptchaPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
  plugins.implements(plugins.IConfigurer, inherit=True)
  plugins.implements(plugins.ITemplateHelpers, inherit=True)
  plugins.implements(plugins.IAuthFunctions, inherit=True)

  def get_auth_functions(self):
        """Redeclare auth functions."""
        return {
            'user_create': textcaptcha_user_create
        }

  def get_helpers(self):
    return {
      'get_textcaptcha': get_textcaptcha,
    }

  def update_config(self, config):
    toolkit.add_template_directory(config, 'templates')
    toolkit.add_resource('fanstatic', 'textcaptcha')


@logic.auth_allow_anonymous_access
def textcaptcha_user_create(context, data_dict=None):
    """Create user."""
    if data_dict:
        a = data_dict.get('textcaptcha')
        a = hashlib.md5(a.lower()).hexdigest() \
            if type(a) in (str, unicode) else '  not valid  '

        v = data_dict.get('textcaptcha_opt')
        log.warn(a)
        log.warn(v)
        if not all([a, v, a in v]):
            raise tk.ValidationError(
                {'spam_prevention': [_('Wrong answer')]}
            )
    return create_auth.user_create(context, data_dict)


def get_textcaptcha():
    """Generate captcha."""
    try:
        captcha_url = config.get('ckan.textcaptcha.url')
        if not captcha_url:
          raise Exception
        resp = requests.get(
            captcha_url
        )
    except Exception:
        textcaptcha = {
            u'q': u'Which digit is 1st in the number 373372?',
            u'a': [
                u'eccbc87e4b5ce2fe28308fd9f2a7baf3',
                u'35d6d33467aae9a2e3dccb4b6b027878'
            ]
        }
    else:
        textcaptcha = resp.json()
    textcaptcha['a'] = ''.join(textcaptcha['a'])
    return textcaptcha
