from streamlit_octostar_research.desktop import whoami
from octostar.client import AuthenticatedClient, check_required_env_vars, set_default_client
import streamlit as st
import hashlib
import os
import json

def get_running_user(prev_user=None, set_as_default=True):
    running_user = whoami()
    if not running_user and prev_user:
        return prev_user
    if not running_user:
        st.stop()
    running_user_hash = hashlib.md5(json.dumps(running_user, sort_keys=True).encode('utf-8'))
    if not prev_user or prev_user['hash'] != running_user_hash:
        ancestor = os.environ.get("OS_ANCESTOR")
        current_pod_name = os.environ.get("OS_CURRENT_POD_NAME")
        if not ancestor and current_pod_name:
            ancestor = current_pod_name[:-6]
        if not ancestor:
            ancestor = "local-dev"
        check_required_env_vars(["OS_API_ENDPOINT", "OS_ONTOLOGY"])
        user = {
            'hash': running_user_hash,
            'name': running_user['username'],
            'client': AuthenticatedClient(
                fixed_token = running_user['os_jwt'],
                timeout = 90,
                base_url = os.environ.get("OS_API_ENDPOINT"),
                headers = {
                    "x-ontology": os.environ.get("OS_ONTOLOGY"),
                    "x-app-name": os.environ.get("OS_APP_NAME", "unknown-local-app"),
                    "x-ancestor": ancestor,
                },
                follow_redirects = True,
                verify_ssl = True,
                raise_on_unexpected_status = False,
            )
        }
        if set_as_default:
            set_default_client(user['client'])
        return user