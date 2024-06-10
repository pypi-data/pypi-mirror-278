from enum import Enum, auto, unique

@unique
class AlertType:
    CONSTANT = auto()

    ZEROS = auto()

    HIGH_CORRELATION = auto()

    HIGH_CARDINALITY = auto()

    IMBALANCE = auto()

    SKEWNESS = auto()

    MISSING_VALUES = auto()

    INFINITE_VALUES = auto()

    SEASONAL = auto()
    
    NON_STATIONARY = auto()

    DATE = auto()

    UNIFORM = auto()

    CONSTANT_LENGTH = auto()

    REJECTED = auto()
    
    UNSUPPORTED = auto()

    DUPLICATES = auto()

    EMPTY = auto()

class Alert:
    def __init__(
            self,
            alert_type: AlertType,
            column_name: str
    ):
        self.alert_type = alert_type
        self.column_name = column_name

    @property
    def alert_name(self) -> str:
        return self.alert_type.name
    
    
    def _alert_meaning(self) -> str:
        return "{} on column: {}".format(self.alert_name, self.column_name)