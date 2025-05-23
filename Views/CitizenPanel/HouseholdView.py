from PySide6.QtGui import QPixmap, QIcon, Qt
from PySide6.QtWidgets import QMessageBox, QFileDialog
from Utils.util_popup import load_popup
from PySide6.QtCore import QDate


class HouseholdView:
    def __init__(self, controller):
        self.controller = controller
        self.popup = None
        self.cp_household_screen = None

    def setup_household_ui(self, ui_screen):
        self.cp_household_screen = ui_screen
        ui_screen.setWindowTitle("MaPro: Household")
        ui_screen.setWindowIcon(QIcon("Resources/Icons/AppIcons/appicon_active_u.ico"))

        # Set icons
        ui_screen.btn_returnToCitizenPanelPage.setIcon(QIcon('Resources/Icons/FuncIcons/img_return.png'))
        ui_screen.cp_HouseholdName_buttonSearch.setIcon(QIcon('Resources/Icons/FuncIcons/icon_search_w.svg'))
        ui_screen.cp_household_button_register.setIcon(QIcon('Resources/Icons/FuncIcons/icon_add.svg'))
        ui_screen.cp_household_button_update.setIcon(QIcon('Resources/Icons/FuncIcons/icon_edit.svg'))
        ui_screen.cp_household_button_remove.setIcon(QIcon('Resources/Icons/FuncIcons/icon_del.svg'))
        ui_screen.householdList_buttonFilter.setIcon(QIcon('Resources/Icons/FuncIcons/icon_filter.svg'))

        # Connect buttons
        ui_screen.btn_returnToCitizenPanelPage.clicked.connect(self.controller.goto_citizen_panel)
        ui_screen.cp_household_button_register.clicked.connect(self.controller.show_register_household_popup)

    def show_register_household_popup(self, parent):
        self.popup = load_popup("Resources/UIs/PopUp/Screen_CitizenPanel/ScreenHousehold/register_household.ui", parent)
        self.popup.setWindowTitle("Mapro: Register New Household")
        self.popup.setWindowModality(Qt.ApplicationModal)
        self.popup.setFixedSize(self.popup.size())

        # Setup popup UI
        self.popup.register_buttonConfirmHousehold_SaveForm.setIcon(QIcon('Resources/Icons//FuncIcons/icon_confirm.svg'))
        self.popup.cp_HomeImageuploadButton.setIcon(QIcon("Resources/Icons/General_Icons/icon_upload_image.svg"))
        self.popup.imageLabel.setAlignment(Qt.AlignCenter)

        date_edit = self.popup.register_household_date_DOV
        date_edit.setDisplayFormat("yyyy-MM-dd")
        date_edit.setDate(QDate.currentDate())  #Default to today
        date_edit.setMaximumDate(QDate.currentDate())

        # Connect popup buttons
        self.popup.register_buttonConfirmHousehold_SaveForm.clicked.connect(self.controller.validate_fields)
        self.popup.cp_HomeImageuploadButton.clicked.connect(self.controller.upload_image)

        # Initialize dropdowns
        self._init_dropdowns()

        return self.popup

    def _init_dropdowns(self):
        # Sitio dropdown
        self.popup.register_household_comboBox_Sitio.clear()
        self.popup.register_household_comboBox_Sitio.addItem("Sitio Uno", "1")
        self.popup.register_household_comboBox_Sitio.addItem("Sitio Dos", "2")
        self.popup.register_household_comboBox_Sitio.addItem("Sitio Tres", "3")

        # Ownership status dropdown
        self.popup.register_household_comboBox_OwnershipStatus.clear()
        self.popup.register_household_comboBox_OwnershipStatus.addItem("Owned")
        self.popup.register_household_comboBox_OwnershipStatus.addItem("Rented")
        self.popup.register_household_comboBox_OwnershipStatus.addItem("Leased")
        self.popup.register_household_comboBox_OwnershipStatus.addItem("Informal Settler")

        # Water source dropdown
        self.popup.register_household_comboBox_WaterSource.clear()
        self.popup.register_household_comboBox_WaterSource.addItem("Level 1- Point Source", "1")
        self.popup.register_household_comboBox_WaterSource.addItem("Level 2 - Communal Faucet", "2")
        self.popup.register_household_comboBox_WaterSource.addItem("Level 3- Individual Connection", "3")
        self.popup.register_household_comboBox_WaterSource.addItem("Others", "4")

        # Toilet type dropdown
        self.popup.register_household_comboBox_ToiletType.clear()
        self.popup.register_household_comboBox_ToiletType.addItem("A - Pour/flush type connected to septic tank", "1")
        self.popup.register_household_comboBox_ToiletType.addItem("B - Pour/flush toilet connected to Sewerage System","2")
        self.popup.register_household_comboBox_ToiletType.addItem("C - Ventilated Pit (VIP) latrine", "3")
        self.popup.register_household_comboBox_ToiletType.addItem("D - Water-sealed toilet", "4")
        self.popup.register_household_comboBox_ToiletType.addItem("E - Overhung latrine", "5")
        self.popup.register_household_comboBox_ToiletType.addItem("F - Open pit latrine", "6")
        self.popup.register_household_comboBox_ToiletType.addItem("G - Without toilet", "7")

    def show_image_preview(self, file_path):
        pixmap = QPixmap(file_path)
        self.popup.imageLabel.setPixmap(
            pixmap.scaled(self.popup.imageLabel.width(),
                          self.popup.imageLabel.height(),
                          Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def show_error_message(self, errors):
        QMessageBox.warning(self.popup, "Incomplete Form",
                            "Please complete all required fields:\n\n• " + "\n• ".join(errors))

    # def highlight_missing_fields(self, errors):
    #     if "Home address is required" in errors:
    #         self.popup.register_household_homeAddress.setStyleSheet("border: 1px solid red;")
    #     if "Sitio is required" in errors:
    #         self.popup.register_household_comboBox_Sitio.setStyleSheet("border: 1px solid red;")
    #     if "Ownership Status is required" in errors:
    #         self.popup.register_household_comboBox_OwnershipStatus.setStyleSheet("border: 1px solid red;")

    def show_success_message(self):
        QMessageBox.information(self.popup, "Success", "Household successfully registered!")

    def show_error_dialog(self, error):
        QMessageBox.critical(self.popup, "Error", f"Failed to register household.\n\n{error}")

    def get_file_path(self):
        return QFileDialog.getOpenFileName(
            self.popup, "Select an Image", "",
            "General_Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )[0]

    def confirm_registration(self):
        reply = QMessageBox.question(
            self.popup,
            "Confirm Registration",
            "Are you sure you want to register this household?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def get_form_data(self):
        return {
            'house_number': self.popup.register_household_homeNumber.text().strip(),
            'home_address': self.popup.register_household_homeAddress.text().strip(),
            'ownership_status': self.popup.register_household_comboBox_OwnershipStatus.currentText(),
            'home_google_link': self.popup.register_household_HomeLink.toPlainText().strip(),
            'interviewer_name': self.popup.register_household_InterviewedBy.text().strip(),
            'reviewer_name': self.popup.register_household_ReviewedBy.text().strip(),
            'date_of_visit': self.popup.register_household_date_DOV.date().toString("yyyy-MM-dd"),
            'water_id': self.popup.register_household_comboBox_WaterSource.currentData(),
            'toilet_id': self.popup.register_household_comboBox_ToiletType.currentData(),
            'sitio_id': self.popup.register_household_comboBox_Sitio.currentData()
        }