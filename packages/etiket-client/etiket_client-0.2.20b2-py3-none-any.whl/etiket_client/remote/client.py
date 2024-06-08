from etiket_client.exceptions import NoAccessTokenFoundException, RequestFailedException,\
    LoginFailedException, TokenRefreshException

from etiket_client.settings.user_settings import user_settings, get_user_data_dir

import datetime, requests, logging, filelock, time

QDL_URL = "https://qdrive.qutech.tudelft.nl:443"
# QDL_URL = "https://0.0.0.0:8000"

PREFIX = "/api/v2"
logger = logging.getLogger(__name__)


class client:
    session = requests.Session()

    @staticmethod
    def url():
        return f"{QDL_URL}{PREFIX}"
    
    @staticmethod
    def __validate():
        user_settings.load() # reload to check if other process already refreshed the credentials
        if user_settings.access_token is None : 
            raise NoAccessTokenFoundException("No access token found, please log in first!")
        
        if user_settings.access_token_expiration <  datetime.datetime.now().timestamp() + 5:
            client._refresh_token()
    
    @staticmethod         
    def __gen_auth_header(headers):
        if headers is dict:
            headers += client.__get_auth_header()
        else:
            headers = client.__get_auth_header()
        return headers

    @staticmethod
    def _login(username : str, password : str):
        logger.info(f"Attemp log in for the user {username}")
        
        data = {"grant_type": "password",
                "username": username,
                "password": password}
        response = client.session.post(f"{QDL_URL}{PREFIX}/token", data=data)

        if response.status_code != 200:
            logger.error(f"Log in failed for {username}\n Server message : {response.json()['detail']} ")
            message = f"Log in failed, please try again. \n\tdetails : {response.json()['detail']}\n"
            raise LoginFailedException(message)
        
        logger.info(f"Log in succesful for {username}\n")
        
        user_settings.user_name = username
        user_settings.access_token = response.json()["access_token"]
        user_settings.refresh_token = response.json()["refresh_token"]
        user_settings.access_token_expiration = int(response.json()["expires_at"])
        user_settings.write()   
    
    @staticmethod
    def _logout():
        try:
            logger.info(f"Logging {user_settings.user_name} out\n")
            # refresh twice to destroy the session id of the token.
            client._refresh_token(user_settings.refresh_token)
            client._refresh_token(user_settings.refresh_token)
            logger.info(f"Logging out succesfull!")
        except Exception as e:
            logger.error(f"Logging of user {user_settings.user_name} not succesfull :/ ({str(e)})\n")
        
        user_settings.access_token = None
        user_settings.refresh_token = None
        user_settings.access_token_expiration = None
        user_settings.user_name = None
        user_settings.write()
    
    @staticmethod
    def _refresh_token(refresh_token : str = None):
        logger.info(f"Refreshing token for {user_settings.user_name}")
        
        try:
            lock =  filelock.FileLock(get_user_data_dir() + 'token_refresh.lock', 2)
            with lock.acquire(0):
                if refresh_token is None:
                    refresh_token = user_settings.refresh_token
                
                data = {"grant_type" : "refresh_token",
                        "refresh_token": refresh_token}
                response = client.session.post(f"{QDL_URL}{PREFIX}/token", data=data)

                if response.status_code != 200:
                    logger.info(f"Token refresh failed. Details : {response.json()['detail']}\n")
                    message = f"Token refresh failed, you will need to login again. \n\tdetails : {response.json()['detail']}\n"
                    raise TokenRefreshException(message)
                
                logger.info(f"Refreshing token for {user_settings.user_name} successfull!")
                
                user_settings.access_token = response.json()["access_token"]
                user_settings.refresh_token = response.json()["refresh_token"]
                user_settings.access_token_expiration = int(response.json()["expires_at"])
                user_settings.write()
        except filelock.Timeout:
            time.sleep(1) # wait a little be be sure that the other process completes.
            client.__validate()
        except Exception as e:
            logger.error(f"Token refresh failed for {user_settings.user_name} :/ ({str(e)})\n")
            raise e         
    
    @staticmethod 
    def post(url, data = None, json_data=None, params=None, headers = None):
        headers = client.__gen_auth_header(headers)
        response = client.session.post(f'{client.url()}{url}',params=params, data=data, json=json_data, headers=headers)
        if response.status_code >=400 and response.status_code <500:
            raise RequestFailedException(response.status_code, response.json()["detail"], response.json()["detail"])
        if response.status_code >=500:
            raise RequestFailedException(response.status_code, "Server error", "Server error")
        return response.json(),

    @staticmethod
    def get(url, params = None, data = None, json_data=None, headers = None):
        headers = client.__gen_auth_header(headers)
        response = client.session.get(f'{client.url()}{url}', params=params, data=data, json=json_data, headers=headers)
        
        if response.status_code >=400 and response.status_code <500:
            raise RequestFailedException(response.status_code, response.json()["detail"], response.json()["detail"])
        if response.status_code >=500:
            raise RequestFailedException(response.status_code, "Server error", "Server error")
        return response.json()
    
    @staticmethod
    def put(url, data = None, params=None, headers = None):
        headers = client.__gen_auth_header(headers)
        response = client.session.put(f'{client.url()}{url}', data=data, params=params, headers=headers)
        if response.status_code >=400:
            raise ValueError
        return response.json()
    
    @staticmethod
    def patch(url, data = None, json_data=None, params=None, headers = None):
        headers = client.__gen_auth_header(headers)
        response = client.session.patch(f'{client.url()}{url}', data=data, json=json_data, headers=headers, params=params)
        if response.status_code >=400:
            raise ValueError
        return response.json()
    
    @staticmethod
    def __get_auth_header():
        client.__validate()
        return {"Authorization": f"Bearer {user_settings.access_token}"}
    
    @staticmethod
    def __get_auth_header_api():
        # TODO
        pass