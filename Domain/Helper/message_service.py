from PySide6.QtWidgets import QMessageBox
from Domain.Helper.i_message_service import IMessageService

class MessageService(IMessageService):
    def __init__(self):
        pass

    def show_dialog(self,message:str,title:str=""):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title if title != "" else "ダイアログ")
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.NoIcon)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msgBox.exec_()

    def show_error(self,message:str,title:str="") -> QMessageBox.StandardButton:
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title if title != "" else "エラー")
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Critical)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes)
        return msgBox.exec_()

    def show_warning(self,message:str,title:str="") -> QMessageBox.StandardButton:
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title if title != "" else "注意")
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Warning)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msgBox.exec_()

    def show_question(self,message:str,title:str="") -> QMessageBox.StandardButton:
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title if title != "" else "確認")
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Question)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        return msgBox.exec_()

    def show_information(self,message:str,title:str="") -> QMessageBox.StandardButton:
        msgBox = QMessageBox()
        msgBox.setWindowTitle(title if title != "" else "情報")
        msgBox.setText(message)
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msgBox.exec_()
