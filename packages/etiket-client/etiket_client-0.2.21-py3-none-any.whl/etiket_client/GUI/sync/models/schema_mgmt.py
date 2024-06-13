from etiket_client.settings.user_settings import user_settings
from etiket_client.python_api.scopes import get_scopes

from PyQt5.QtCore import QAbstractListModel, Qt, pyqtSlot, pyqtProperty

class schema_manager(QAbstractListModel):
    name =Qt.UserRole + 1
    fixed_values = Qt.UserRole + 2
    values = Qt.UserRole + 3
    selected_value = Qt.UserRole + 4

    def __init__(self, model_data, parent=None):
        super().__init__(parent)
        self._data = model_data

    @pyqtSlot(result = str)
    def getCurrentUser(self):
        return user_settings.user_name

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, QModelIndex, role):
        row = QModelIndex.row()
        if role == self.name:
            return self._data[row]['name']
        if role == self.fixed_values:
            return self._data[row]['fixed_values']
        if role == self.values:
            return self._data[row]['values']
        if role == self.selected_value:
            return self._data[row]['selected_value']

    def roleNames(self):
        return {
            Qt.UserRole + 1: b'name',
            Qt.UserRole + 2: b'fixed_values',
            Qt.UserRole + 3: b'values',
            Qt.UserRole + 4: b'selected_value',
        }

    def reset_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()
