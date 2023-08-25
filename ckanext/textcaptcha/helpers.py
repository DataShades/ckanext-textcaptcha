import requests

import ckan.plugins.toolkit as tk


def get_textcaptcha():
    """Generate text captcha."""
    try:
        captcha_url = tk.config["ckan.textcaptcha.url"]

        resp = requests.get(captcha_url)
    except Exception:
        textcaptcha = {
            "q": "Which digit is 1st in the number 373372?",
            "a": [
                "eccbc87e4b5ce2fe28308fd9f2a7baf3",
                "35d6d33467aae9a2e3dccb4b6b027878",
            ],
        }
    else:
        textcaptcha = resp.json()

    textcaptcha["a"] = "".join(textcaptcha["a"])

    return textcaptcha
