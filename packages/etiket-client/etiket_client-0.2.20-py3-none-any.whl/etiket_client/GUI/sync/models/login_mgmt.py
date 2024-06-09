from etiket_client.remote.authenticate import _host_online, _is_logged_in, login, logout
from etiket_client.settings.user_settings import user_settings

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, pyqtProperty

class login_manager(QObject):
    loginChanged = pyqtSignal(name="loginChanged")
    _is_loggedIn = False
    _is_online = False
    
    def __init__(self, parent: 'QObject | None' = None):
        super().__init__(parent)
        self._is_online = _host_online()
        if self._is_online:
            self._is_loggedIn = _is_logged_in()
    
    @pyqtProperty(bool, notify=loginChanged)
    def loggedIn(self):
        return self._is_loggedIn

    @pyqtSlot(result = str)
    def getCurrentUser(self):
        return user_settings.user_name

    def change_state(self, _is_loggedIn):
        if self._is_loggedIn == _is_loggedIn:
            return
        self._is_loggedIn = _is_loggedIn
        self.loginChanged.emit()

    @pyqtSlot(str, str, result=bool)
    def login(self, username, password):
        try:
            login(username, password)
            self.change_state(True)
            return True
        except Exception as e:
            print(e)
            print("Login in failed. Please try again.")
            return False

    @pyqtSlot()
    def logout(self):
        logout()
        self.change_state(False)