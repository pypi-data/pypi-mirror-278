from etiket_client.remote.client import client
from etiket_client.remote.endpoints.models.user import UserReadWithScopes

def user_read_me() -> UserReadWithScopes:
    response = client.get("/user/me/")
    return UserReadWithScopes.model_validate(response)