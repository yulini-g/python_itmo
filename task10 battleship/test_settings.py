import sys
from PySide6.QtWidgets import QApplication
from gui.settings_dialog import SettingsDialog

app = QApplication(sys.argv)
print("Создаём диалог...")
dialog = SettingsDialog()
print("Диалог создан, показываем...")
dialog.show()
print("Диалог показан")
sys.exit(app.exec())