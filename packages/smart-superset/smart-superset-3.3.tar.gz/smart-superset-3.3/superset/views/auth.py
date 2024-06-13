
from flask import flash, redirect, request, url_for
from superset.extensions import appbuilder
from flask_login import login_user

from superset import app

import time
import base64
import hmac

import logging


import functools

from flask_appbuilder.const import PERMISSION_PREFIX

log = logging.getLogger(__name__)

def generate_token(key, expire=3600):
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

def certify_token(key, token):
    try:
        token_str = base64.urlsafe_b64decode(token).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return False
        ts_str = token_list[0]
        if float(ts_str) < time.time():
            return False
        known_sha1_tsstr = token_list[1]
        sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
        calc_sha1_tsstr = sha1.hexdigest()
        if calc_sha1_tsstr != known_sha1_tsstr:
            return False
        return True
    except Exception as e:
        print(str(e.args))
        return False

def has_access(f):
    """
    Use this decorator to enable granular security permissions to your methods.
    Permissions will be associated to a role, and roles are associated to users.

    By default the permission's name is the methods name.
    """
    if hasattr(f, "_permission_name"):
        permission_str = f._permission_name
    else:
        permission_str = f.__name__

    def wraps(self, *args, **kwargs):
        permission_str = f"{PERMISSION_PREFIX}{f._permission_name}"
        if self.method_permission_name:
            _permission_name = self.method_permission_name.get(f.__name__)
            if _permission_name:
                permission_str = f"{PERMISSION_PREFIX}{_permission_name}"
        if permission_str in self.base_permissions and self.appbuilder.sm.has_access(
            permission_str, self.class_permission_name
        ):
            return f(self, *args, **kwargs)
        else:
            if request.method == 'GET' and request.args.get("user") and request.args.get("EmbedToken"):
                username = request.args.get("user")
                token = request.args.get("EmbedToken")
                if certify_token(app.config.get('APPKEY') + username, token):
                    user = appbuilder.sm.auth_user_remote_user(username)
                    if user is None:
                        access_denied = 'auth fail, no user setup'
                    else:
                        login_user(user)
                        return redirect(
                            request.args.get("next") or appbuilder.get_url_for_index)
                else:
                    access_denied = 'token auth fail'
            else:
                access_denied = "Access is Denied"
            flash(access_denied, "danger")
        return redirect(
            url_for(
                self.appbuilder.sm.auth_view.__class__.__name__ + ".login",
                next=request.url,
            )
        )

    f._permission_name = permission_str
    return functools.update_wrapper(wraps, f)
