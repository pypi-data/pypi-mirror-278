from etiket_client.settings.user_settings import user_settings
from etiket_client.exceptions import LoginFailedException, TokenRefreshException
from etiket_client.remote.client import client, QDL_URL, PREFIX

from etiket_client.sync.backends.native.sync_user import sync_current_user
from etiket_client.sync.backends.native.sync_scopes import sync_scopes
from etiket_client.local.database import Session

from getpass import getpass

import logging, socket

logger = logging.getLogger(__name__)

def authenticate_with_console(_n_tries = 0):
    print("Please enter your username ::")
    username = input()
    print("Please enter your password ::")
    password = getpass()
    
    try:
        login(username, password)     
        print(f"Log in succesful. Welcome {username}!")
    except Exception as e:
        print(f'Failed log in with error: {e}')
        logger.exception(f"Failed to log in with username {username}.\n")
        if _n_tries > 2:
            pass
        else:
            authenticate_with_console(_n_tries=_n_tries+1)

def login(username : str, password : str):
    client._login(username, password)
    with Session() as session:
        sync_current_user(session)
        sync_scopes(session)

def _is_logged_in():
    # try to refresh token to see if user is online.
    logger.info(f"Checking if host is logged in by refreshing the token.")
    try:
        client._refresh_token()
        return True
    except:
        return False

def _host_online():
    # checks if a connection ot the QDL server can be made.
    socket.setdefaulttimeout(0.5)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = QDL_URL.rsplit(":", 1)
    address[0] = address[0].split("://", 1)[1]
    address[1] = int(address[1])

    result = sock.connect_ex(tuple(address))
    if result == 0:
        return True

    logger.info(f"Host offline")
    return False
        
def logout():
    client._logout()
