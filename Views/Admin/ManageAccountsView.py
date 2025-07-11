from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from Utils.util_popup import load_popup


class ManageAccountsView:
    def __init__(self, controller):
        self.controller = controller
        self.manage_accounts_screen = None

    def setup_manage_accounts_ui(self, ui_screen):
        self.manage_accounts_screen = ui_screen
        self._setup_navigation_assets()
        self._connect_buttons()

    def show_register_account_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminPanel/register_account.ui", parent)
        self.popup.setWindowTitle("Mapro: Register New System User")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.register_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.register_buttonConfirmAccount_SaveForm.clicked.connect(self.controller.validate_fields)
        self._init_dropdowns()
        self.popup.show()
        return self.popup

    def show_update_account_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_Admin/AdminPanel/Update/edit_register_account.ui", parent)
        self.popup.setWindowTitle("Mapro: Update System User")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())
        self.popup.edit_buttonConfirmAccount_SaveForm.setIcon(QIcon('Resources/Icons/FuncIcons/icon_confirm.svg'))
        self.popup.edit_buttonConfirmAccount_SaveForm.clicked.connect(self.controller.validate_update_fields)
        self._init_dropdowns()
        self._init_status_dropdown()

        self.popup.input_id_search.textChanged.connect(self.controller.handle_system_user_search)
        self.popup.show()
        return self.popup

    def get_form_data(self):
        return {
            'first_name': self.popup.RegAcc_input_fname.text().strip(),
            'last_name': self.popup.RegAcc_input_lname.text().strip(),
            'middle_name': self.popup.RegAcc_input_mname.text().strip(),
            'user_password': self.popup.RegAcc_input_PIN.text().strip(),
            'confirm_password': self.popup.RegAcc_confirm_PIN.text().strip(),
            'role': self.popup.RegAcc_select_role.currentText().strip()
        }

    def get_update_form_data(self):
        return {
            'first_name': self.popup.RegAcc_input_fname.text().strip(),
            'last_name': self.popup.RegAcc_input_lname.text().strip(),
            'middle_name': self.popup.RegAcc_input_mname.text().strip(),
            'user_password': self.popup.RegAcc_input_PIN.text().strip(),
            'confirm_password': self.popup.RegAcc_confirm_PIN.text().strip(),
            'role': self.popup.RegAcc_select_role.currentText().strip(),
            'status':self.popup.RegAcc_select_status.currentText().strip()
        }


    def show_success_message(self, title, message):
        QMessageBox.information(self.popup, title, message)

    def show_error_dialog(self, error):
        QMessageBox.critical(self.popup, "Error", f"Failed to register System User.\n\n{error}")

    def confirm_registration(self, title, message):
        reply = QMessageBox.question(
            self.popup,
            title,
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def _setup_navigation_assets(self):
        self.manage_accounts_screen.btn_returnToAdminPanelPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        self.manage_accounts_screen.admn_button_RegAcc.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        self.manage_accounts_screen.admn_button_UpdAcc.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        self.manage_accounts_screen.admn_button_RemAcc.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        self.manage_accounts_screen.buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))

    def _connect_buttons(self):
        self.manage_accounts_screen.btn_returnToAdminPanelPage.clicked.connect(self.controller.goto_admin_panel)
        self.manage_accounts_screen.admn_button_RegAcc.clicked.connect(
            lambda: self.show_register_account_popup(self.manage_accounts_screen)
        )
        self.manage_accounts_screen.admn_button_UpdAcc.clicked.connect(
            lambda: self.show_update_account_popup(self.manage_accounts_screen)
        )
        self.manage_accounts_screen.admn_button_RemAcc.clicked.connect(self.controller.handle_remove_user)

    def _init_dropdowns(self):
        self.popup.RegAcc_select_role.clear()
        self.popup.RegAcc_select_role.addItems(["Staff", "Admin"])

    def _init_status_dropdown(self):
        self.popup.RegAcc_select_status.clear()
        self.popup.RegAcc_select_status.addItems(["Active", "Inactive"])