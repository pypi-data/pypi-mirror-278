from glxeveloop.hooks import Hooks


class HooksProperty:
    debug: bool

    def __init__(self) -> None:
        self.__hooks = Hooks()

    @property
    def hooks(self):
        return self.__hooks

    @hooks.setter
    def hooks(self, value):
        if value is None:
            value = Hooks()
        if not isinstance(value, Hooks):
            raise TypeError("'hooks' property value must be a Hooks instance or None")
        if value != self.hooks:
            self.__hooks = value
