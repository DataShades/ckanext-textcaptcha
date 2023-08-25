from __future__ import annotations

import hashlib
import logging

import ckan.plugins.toolkit as tk
from ckan import types

log = logging.getLogger(__name__)


@tk.auth_allow_anonymous_access
@tk.chained_auth_function
def user_create(
    next_func: types.AuthFunction,
    context: types.Context,
    data_dict: types.DataDict | None,
) -> types.AuthResult:
    if data_dict:
        answer = str(data_dict.get("textcaptcha", ""))
        answer = hashlib.md5(answer.lower().encode("utf-8")).hexdigest()

        captcha_options = data_dict.get("textcaptcha_opt", "")

        if not all([answer, captcha_options, answer in captcha_options]):
            log.warn(answer)
            log.warn(captcha_options)

            raise tk.ValidationError({"spam_prevention": [tk._("Wrong answer")]})

    if data_dict is None:
        data_dict = {}

    return next_func(context, data_dict)
