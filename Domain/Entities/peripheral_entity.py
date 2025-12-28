class PeripheralEntity():
    def __init__(self, device_name:str, mac_address:str):
        self._device_name:str = device_name
        self._mac_address:str = mac_address

    @property
    def device_name(self) -> str:
        return self._device_name

    # @property.setter
    # def device_name(self,value:str):
    #     self._device_name = value

    @property
    def mac_address(self) -> str:
        return self._mac_address

    @property
    def display_peripheral_name(self) ->str:
        return f"{self.device_name} / {self.mac_address}"

    def __str__(self):
        return f"{self.device_name} / {self.mac_address}"