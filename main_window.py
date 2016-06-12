import datetime

from PyQt4 import QtGui, QtCore

import ui.loading_dialog_ui
import ui.main_window_ui
from pyuarm import *
from pyuarm.calibrate import Calibration

__version__ = "1.0"

style_none = "background-color:transparent; border:1px"
style_circle_red = "background-color: rgb(200,0,0) ;border-radius: 12px"
style_circle_green = "background-color: rgb(0,200,0) ;border-radius: 12px"
style_circle_yellow = "background-color: rgb(230,230,0) ;border-radius: 12px "

style_connection_red = "background-color: rgb(200,0,0) ;border-radius: 15px"
style_connection_green = "background-color: rgb(0,200,0) ;border-radius: 15px"
style_connection_yellow = "background-color: rgb(230,230,0) ; border-radius: 15px"

style_confirm_red = "background-color: rgb(200,0,0) ;border-radius: 17px "
style_confirm_green = "background-color: rgb(0,200,0);border-radius: 17px "
style_confirm_yellow = "background-color: rgb(230,230,0);border-radius: 17px "


class LoadingDialog(QtGui.QDialog, ui.loading_dialog_ui.Ui_loadingWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)


class MainWindow(QtGui.QMainWindow, ui.main_window_ui.Ui_mainWindow):
    uarm = None
    calibration = None
    label_linear_servo_intercept = []
    label_linear_servo_slope = []
    label_manual_calibration_offset = []
    frame_manual_flag = []
    frame_linear_flag = []
    is_available = False
    default_log_file_path = "uarm_calibration.log"
    log_file = None
    calibration_start_flag = False

    def __init__(self):
        loadingDialog = LoadingDialog()
        loadingDialog.show()
        QtGui.QApplication.processEvents()
        self.log_file = open(self.default_log_file_path, 'a')
        super(self.__class__, self).__init__()
        self.setupUi(self)
        menubar = self.menubar
        menubar.setNativeMenuBar(False)
        self.refresh_uarm()
        self.active_button()
        loadingDialog.close()
        loadingDialog.destroy()
        if self.uarm is not None:
            self.write_notification(self.tr("Waiting For Next Action"))

    def active_button(self):
        self.button_calibration_start.clicked.connect(self.start_all_calibration)
        self.button_manual_calibration_confirm.clicked.connect(self.confirm_manual_calibration)
        self.action_start.triggered.connect(self.start_all_calibration)
        self.action_fresh.triggered.connect(self.refresh_uarm)
        self.action_quit.triggered.connect(self.quit_menu_action)

    def quit_menu_action(self):
        QtCore.QCoreApplication.instance().quit()

    # Confirm the Manual Calibration
    def confirm_manual_calibration(self):
        self.calibration.manual_operation_trigger = False

    def clear_all(self):
        self.uarm = None
        self.calibration = None
        self.label_linear_servo_intercept = []
        self.label_linear_servo_slope = []
        self.label_manual_calibration_offset = []
        self.frame_manual_flag = []
        self.frame_linear_flag = []

    def refresh_uarm(self):
        self.uf_print(self.tr("Trying to Reconnect uArm"))
        self.clear_all()
        QtGui.QApplication.processEvents()
        self.init_ui_text()
        self.init_port()
        self.init_uarm_sn()

    def init_port(self):
        ports = uarm_ports()
        self.uarm = None
        self.calibration = None
        if len(ports) > 0:
            self.uarm = get_uarm()
            self.calibration = Calibration(self.uarm, self.uf_print)
            self.label_port_val.setText(self.uarm.port)
            fw_version = self.uarm.firmware_version
            self.label_firmware_version_val.setText(fw_version)
            self.uf_print(self.tr("Connect to Port: " + self.uarm.port))
        else:
            self.uf_print(self.tr("Please Connect uArm"))

    def init_uarm_sn(self):
        if self.uarm is not None:
            if self.uarm.read_eeprom(EEPROM_DATA_TYPE_BYTE, SERIAL_NUMBER_ADDRESS) == CONFIRM_FLAG:
                sn = self.uarm.read_serial_number()
                self.label_uarm_sn_val.setText(sn)
            else:
                self.label_uarm_sn_val.setText("N/A")
        else:
            self.label_uarm_sn_val.setText("N/A")


    def uf_print(self, msg):
        self.write_notification(msg)

    def quit_menu_action(self):
        QtCore.QCoreApplication.instance().quit()

    def start_all_calibration(self):
        if self.uarm is not None:
            if self.uarm.is_connected():
                if not self.calibration_start_flag:
                    self.calibration.calibrate_all(self.linear_calibration_start, self.manual_calibration_start, self.stretch_calibration_start)
                    self.calibration_start_flag = False
                else:
                    show_message_box(self.tr("Calibration is already start!"))
            else:
                show_message_box(self.tr("uArm is disconnected, Please check!"))
        else:
            show_message_box(self.tr("Please Connect uArm First"))

    def init_ui_text(self):

        self.label_linear_servo_intercept.append(self.label_linear_servo1_intercept)
        self.label_linear_servo_intercept.append(self.label_linear_servo2_intercept)
        self.label_linear_servo_intercept.append(self.label_linear_servo3_intercept)
        self.label_linear_servo_intercept.append(self.label_linear_servo4_intercept)

        self.label_linear_servo_slope.append(self.label_linear_servo1_slope)
        self.label_linear_servo_slope.append(self.label_linear_servo2_slope)
        self.label_linear_servo_slope.append(self.label_linear_servo3_slope)
        self.label_linear_servo_slope.append(self.label_linear_servo4_slope)

        self.frame_linear_flag.append(self.f_linear_servo1_flag)
        self.frame_linear_flag.append(self.f_linear_servo2_flag)
        self.frame_linear_flag.append(self.f_linear_servo3_flag)
        self.frame_linear_flag.append(self.f_linear_servo4_flag)

        self.label_manual_calibration_offset.append(self.label_manual_servo1_value)
        self.label_manual_calibration_offset.append(self.label_manual_servo2_value)
        self.label_manual_calibration_offset.append(self.label_manual_servo3_value)

        self.frame_manual_flag.append(self.f_manual_servo1_flag)
        self.frame_manual_flag.append(self.f_manual_servo2_flag)
        self.frame_manual_flag.append(self.f_manual_servo3_flag)
        self.f_linear_servo1_flag.setStyleSheet(style_none)
        self.f_linear_servo2_flag.setStyleSheet(style_none)
        self.f_linear_servo3_flag.setStyleSheet(style_none)
        self.f_linear_servo4_flag.setStyleSheet(style_none)
        self.f_manual_servo1_flag.setStyleSheet(style_none)
        self.f_manual_servo2_flag.setStyleSheet(style_none)
        self.f_manual_servo3_flag.setStyleSheet(style_none)
        self.f_stretch_left_flag.setStyleSheet(style_none)
        self.f_stretch_right_flag.setStyleSheet(style_none)
        self.button_manual_calibration_confirm.setVisible(False)

    # Start Linear Calibration
    def linear_calibration_start(self):
        self.write_notification(self.tr("Calibrating Linear Offset"))
        if self.uarm is not None:
            if self.uarm.is_connected():
                self.calibration.linear_calibration_section(self.check_linear_completed)
                self.write_notification(self.tr("Linear Offset Calibration Completed"))
                self.calibration.init_calibration_completed_flag()

    # Check if Linear Calibration is Completed, If calibration completed, Mark flag frame green
    def check_linear_completed(self, seq, linear_is_correct, linear_offset_data):
        self.label_linear_servo_intercept[seq].setText(str(linear_offset_data['INTERCEPT']))
        self.label_linear_servo_slope[seq].setText(str(linear_offset_data['SLOPE']))
        if linear_is_correct:
            self.frame_linear_flag[seq].setStyleSheet(style_circle_green)
        else:
            self.frame_linear_flag[seq].setStyleSheet(style_circle_yellow)

    # Start Manual Calibration
    def manual_calibration_start(self):
        if self.calibration.is_linear_calibrated:
            self.write_notification(self.tr("Manual Calibration Start"))
            if self.uarm is not None:
                if self.uarm.is_connected():
                    self.calibration.manual_calibration_section(self.check_manual_completed)
                    self.write_notification(self.tr("Manual Calibration Completed"))
                    self.button_manual_calibration_confirm.setVisible(False)
                    self.calibration.init_calibration_completed_flag()
        else:
            show_message_box(self.tr("Please Complete Linear Calibration First"))

    # Check if Manual Calibration is completed, if calibration completed, Mark flag frame green
    def check_manual_completed(self, manual_servo_offset, manual_servo_offset_correct_flag):
        self.button_manual_calibration_confirm.setVisible(True)
        servo_offset_data = manual_servo_offset
        manual_servo_offset_correct_flag = manual_servo_offset_correct_flag
        for i in range(3):
            self.label_manual_calibration_offset[i].setText(str(servo_offset_data[i]))
            if manual_servo_offset_correct_flag[i]:
                self.frame_manual_flag[i].setStyleSheet(style_circle_green)
            else:
                self.frame_manual_flag[i].setStyleSheet(style_circle_yellow)

    # Start Stretch Calibration
    def stretch_calibration_start(self):
        if not self.calibration.stretch_calibration_flag:
            if self.calibration.is_manual_calibrated:
                self.write_notification(self.tr("Stretch Offset Calibration Start"))
                self.stretch_calibration_flag = True
                if self.uarm is not None:
                    if self.uarm.is_connected():
                        self.calibration.stretch_calibration_section(self.check_stretch_offset_completed)
                        self.write_notification(self.tr("Stretch Offset Calibration Completed"))
                        self.calibration.init_calibration_completed_flag()
            else:
                show_message_box(self.tr("Please Complete Manual Calibration First"))
        else:
            self.calibration.stretch_calibration_flag = False

    # Check if Stretch Calibration is completed, if calibration completed, Mark flag frame green
    def check_stretch_offset_completed(self, servo_offset, servo_offset_correct_flag):
        if servo_offset_correct_flag[0]:
            self.label_stretch_left_value.setText(str(servo_offset['LEFT']))
            self.f_stretch_left_flag.setStyleSheet(style_circle_green)
        else:
            self.f_stretch_left_flag.setStyleSheet(style_circle_yellow)
        if servo_offset_correct_flag[1]:
            self.label_stretch_right_value.setText(str(servo_offset['RIGHT']))
            self.f_stretch_right_flag.setStyleSheet(style_circle_green)
        else:
            self.f_stretch_right_flag.setStyleSheet(style_circle_yellow)

    # Confirm the Manual Calibration
    def confirm_manual_calibration(self):
        self.calibration.manual_operation_trigger = False

    # write the Text into Notification Zone
    def write_notification(self, msg):
        self.label_notify.setText(msg)
        QtGui.QApplication.processEvents()
        now = "[" + str(datetime.datetime.now()) + "]:"
        self.log_file.writelines(now + msg + '\n')

def show_message_box(msg):
    msgBox = QtGui.QMessageBox()
    msgBox.setText(msg)
    msgBox.exec_()
