import datetime
from app.logger import log


class Interval:

    def __init__(self):

        # For the future: make generic Interval so you could use it in any type of a timer
        # self._hours: int = 0
        # self._minutes: int = 0
        # self._seconds: int = 0

        self._name: str = ""
        self._value: int = 0      # Minutes
        self._type: str = ""      # I don't know if I need this or not anymore
        self._remaining: int = 0  # Time remaining in seconds

    def create(self, name: str, value: int, type: str):  # Create new interval
        self.name = name
        self.value = value
        self._type = type  # I still don't have setter fo this prop

    def drop(self):  # Change all values to defaults
        self._name: str = ""
        self._value: int = 0  # Minutes
        self._type: str = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value:
            self._name = value
        else:
            log.error("Interval must be > 0. Interval set back to 0")
            self._name = ""

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def name(self, value):
        if value >= 0:
            self._value = value
        else:
            log.error("Interval must be > 0. Interval set back to 0")
            self._value = 0

    def seconds(self):  # Convert minutes to seconds
        return self._value * 60

    def time(self):  # Make correct time with datetime module
        if self._value >= 0:
            return datetime.timedelta(seconds=self.seconds(self._value))
        else:
            return datetime.timedelta(seconds=0)

    def to_string(self):
        return str(self._value)

    def to_json(self):
        pass
