import datetime
class LogFileEntity():
    def __init__(self, name:str):
        self._file_name:str = name

    @property
    def file_name(self) -> str:
        return self._file_name

    def __str__(self):
        return f"{self.file_name[:4]}-{self._file_name[4:6]}-{self._file_name[6:]}"

    # @property.setter
    # def device_name(self,value:str):
    #     self._device_name = value

    # @property
    # def display_peripheral_name(self) ->str:
    #     return f"{self.device_name} / {self.mac_address}"