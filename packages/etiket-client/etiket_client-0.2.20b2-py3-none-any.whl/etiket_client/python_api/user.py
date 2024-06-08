from etiket_client.settings.user_settings import user_settings

def get_current_user():
    if user_settings.user_name is None:
        raise ValueError("TODO define error with helpful text")
    return user_settings.user_name
