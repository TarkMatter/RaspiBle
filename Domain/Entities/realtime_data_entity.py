import datetime
class RealTimeDataEntity():
    def __init__(self, now:datetime, current:float):
        self._now:datetime = now
        self._current:float = current

    @property
    def now(self) -> datetime:
        return self._now

    # @property.setter
    # def device_name(self,value:str):
    #     self._device_name = value

    @property
    def current(self) -> float:
        return self._current

    # @property
    # def display_peripheral_name(self) ->str:
    #     return f"{self.device_name} / {self.mac_address}"