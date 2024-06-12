import contextvars
import logging
import os

ClsKey = "x-aily-cls"

CtxVar = contextvars.ContextVar(ClsKey)

try:
    from _sys import CtxVar  # type: ignore
except Exception as e:
    logging.info(f'fail to load CtxVar {e}')


def ctx():
    return contextvars.copy_context()


def get_ctx():
    try:
        return CtxVar.get()
    except LookupError:
        CtxVar.set({})
        return CtxVar.get()


def get_ctx_key(key):
    try:
        return get_ctx()[key]
    except Exception as err:
        logging.info(f'key `{key}` not found in context {err}')
        return None


def get_from_credential(key: str):
    credential = get_ctx_key("credential")
    if credential is None:
        return ""
    return credential[key]


def is_local_dev():
    return os.environ.get("AILY_SDK_LOCAL_DEBUG") == "true"


def get_client_id():
    if is_local_dev():
        return os.environ.get("AILY_SDK_CLIENT_ID")
    return get_from_credential("clientID")


def get_client_secret():
    if is_local_dev():
        return os.environ.get("AILY_SDK_CLIENT_SECRET")
    return get_from_credential("clientSecret")


def get_domain():
    if is_local_dev():
        return os.environ.get("AILY_SDK_DOMAIN")
    return get_from_credential("domain")


def get_by_headers(key):
    headers = get_ctx_key("sysHeaders")
    if headers is None:
        return ""
    return headers.get(key)
