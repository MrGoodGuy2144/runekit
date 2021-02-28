from typing import TYPE_CHECKING

from PySide2.QtCore import Slot, Signal, QCoreApplication
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QSystemTrayIcon, QMenu

if TYPE_CHECKING:
    from runekit.host import Host


class TrayIcon(QSystemTrayIcon):
    on_settings = Signal()

    host: "Host"

    def __init__(self, host: "Host"):
        global _tray_icon
        super().__init__(QIcon(":/runekit/ui/trayicon.png"))

        _tray_icon = self

        self.host = host
        self._setup_menu()
        self.setContextMenu(self.menu)

    def _setup_menu(self):
        if not hasattr(self, "menu"):
            self.menu = QMenu("RuneKit")

        self.menu.clear()

        for app_id, manifest in self.host.app_store:
            app_menu = self.menu.addAction(manifest["appName"])
            app_menu.triggered.connect(
                lambda _=None, app_id=app_id: self.host.launch_app_id(app_id)
            )

            icon = self.host.app_store.icon(app_id)
            if icon:
                app_menu.setIcon(icon)

        self.menu.addSeparator()
        self.menu_settings = self.menu.addAction("Settings")
        self.menu_settings.triggered.connect(self.on_settings)
        self.menu.addAction("Exit", lambda: QCoreApplication.instance().quit())

    @Slot()
    def update_menu(self):
        self._setup_menu()


def tray_icon() -> TrayIcon:
    return _tray_icon
