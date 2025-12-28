from abc import ABCMeta, abstractmethod

from PySide6.QtWidgets import QMessageBox

class IMessageService(metaclass=ABCMeta):
    """
    Interface for the MesseageService repository.
    """

    @abstractmethod
    def show_dialog(self,message:str,title:str=""):
        raise NotImplementedError("show_dialog method must be implemented")

    @abstractmethod
    def show_error(self,message:str,title:str="") -> QMessageBox.StandardButton:
        raise NotImplementedError("show_error method must be implemented")

    @abstractmethod
    def show_warning(self,message:str,title:str="") -> QMessageBox.StandardButton:
        raise NotImplementedError("show_warning method must be implemented")

    @abstractmethod
    def show_question(self,message:str,title:str="") -> QMessageBox.StandardButton:
        raise NotImplementedError("show_question method must be implemented")

    @abstractmethod
    def show_information(self,message:str,title:str="") -> QMessageBox.StandardButton:
        raise NotImplementedError("show_information method must be implemented")