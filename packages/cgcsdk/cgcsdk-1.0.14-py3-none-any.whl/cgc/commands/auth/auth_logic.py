import os
from cgc.utils.config_utils import get_config_path


from cgc.utils import get_headers_data, prepare_headers
from cgc.utils.consts.env_consts import TMP_DIR
from cgc.utils.requests_helper import call_api, EndpointTypes
from cgc.utils.response_utils import retrieve_and_validate_response_send_metric
from cgc.utils.config_utils import save_to_config

TMP_DIR_PATH = os.path.join(get_config_path(), TMP_DIR)


def auth_delete_api_key(api_key: str, user_id: str = None, password: str = None):
    """Function to delete API key."""
    url = f"{get_headers_data.load_user_api_url()}/v1/api/user/delete/api-key?api_key={api_key}"
    headers = prepare_headers.prepare_headers_api_key(user_id, password)
    metric = "auth.api-key"
    __res = call_api(
        request=EndpointTypes.delete,
        url=url,
        headers=headers,
    )

    json_data = retrieve_and_validate_response_send_metric(__res, metric)
    return json_data["details"]


def auth_list_api_keys(user_id: str = None, password: str = None):
    """Function to list API keys."""
    url = f"{get_headers_data.load_user_api_url()}/v1/api/user/list/api-key"
    headers = prepare_headers.prepare_headers_api_key(user_id, password)
    metric = "auth.api-key"
    __res = call_api(
        request=EndpointTypes.get,
        url=url,
        headers=headers,
    )

    json_data = retrieve_and_validate_response_send_metric(__res, metric)
    return json_data["details"].get("api_keys")


def auth_create_api_key_with_save(user_id: str = None, password: str = None):
    """Function to create API key and API secret for user and save it to config file."""
    url = f"{get_headers_data.load_user_api_url()}/v1/api/user/create/api-key"
    headers = prepare_headers.prepare_headers_api_key(user_id, password)
    metric = "auth.api-key"
    __res = call_api(
        request=EndpointTypes.post,
        url=url,
        headers=headers,
    )

    json_data = retrieve_and_validate_response_send_metric(__res, metric)
    api_key = json_data["details"].get("_id")
    secret = json_data["details"].get("secret")
    save_to_config(api_key=api_key, api_secret=secret)
    if user_id is not None and password is not None:
        save_to_config(user_id=user_id, password=password)
    return api_key, secret
