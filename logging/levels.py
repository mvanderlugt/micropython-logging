class Levels:
    TRACE = 1
    DEBUG = 2
    INFO = 3
    WARNING = 4
    ERROR = 5
    OFF = 100

    __lookup = {
        TRACE: 'TRACE',
        DEBUG: 'DEBUG',
        INFO: 'INFO',
        WARNING: 'WARNING',
        ERROR: 'ERROR',
        OFF: 'OFF'
    }

    @staticmethod
    def get_level(search: str) -> int:
        for level, name in Levels.__lookup.items():
            if name == search:
                return level

    @staticmethod
    def get_name(level: int) -> str:
        return Levels.__lookup.get(level)
