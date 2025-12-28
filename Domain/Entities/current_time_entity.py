import datetime
class CurrentTimeEntity():
    def __init__(self, now:datetime):
        self._current_time:datetime = now

    @property
    def current_time(self) -> datetime:
        return self._current_time

    # @property.setter
    # def device_name(self,value:str):
    #     self._device_name = value

    # @property
    # def display_peripheral_name(self) ->str:
    #     return f"{self.device_name} / {self.mac_address}"