from etiket_client.local.dao.scope import dao_scope, ScopeReadWithUsers
from etiket_client.local.database import Session

from etiket_client.settings.user_settings import user_settings
from etiket_client.sync.backends.native.sync_scopes import sync_scopes

from typing import List

def get_selected_scope() -> ScopeReadWithUsers:
    with Session() as session:
        sync_scopes(session)
        current_scope = dao_scope.read(user_settings.current_scope, session)
    return current_scope

def get_scopes() -> List[ScopeReadWithUsers]:
    with Session() as session:
        sync_scopes(session)
        scopes = dao_scope.read_all(username=user_settings.user_name,
                                    session=session)
    return scopes