import requests

import ckan.plugins.toolkit as tk

if tk.check_ckan_version("2.9"):
    config = tk.config
else:
    from pylons import config


def get_textcaptcha():
    """Generate captcha."""
    try:
        captcha_url = config.get("ckan.textcaptcha.url")
        if not captcha_url:
            raise Exception
        resp = requests.get(captcha_url)
    except Exception:
        textcaptcha = {
            u"q": u"Which digit is 1st in the number 373372?",
            u"a": [
                u"eccbc87e4b5ce2fe28308fd9f2a7baf3",
                u"35d6d33467aae9a2e3dccb4b6b027878"
            ]
        }
    else:
        textcaptcha = resp.json()

    textcaptcha["a"] = "".join(textcaptcha["a"])
    return textcaptcha


def get_helpers():
    return dict(
        get_textcaptcha=get_textcaptcha
    )
