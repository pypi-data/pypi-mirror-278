
from datetime import datetime

class logger:

    def __init__(self, app_name : str, function_name : str = "main" , mute : bool = False ) -> None:
        self._app_name = app_name
        self._function_name = function_name
        self._start_at = datetime.now()
        if not mute:
            self.INFO(f"Starting function {self._function_name} at {self._start_at}")

    def start_function(self, function_name : str, mute : bool = False):
        return logger(self._app_name, function_name, mute)
    
    def end_function(self) -> None:
        message = f"Function {self._function_name} ended - time {(datetime.now() - self._start_at).total_seconds()} Seconds"
        self.INFO(message)

    def INFO(self, message : str) -> None:
        self._print("INFO", message)

    def WARNING(self, message : str) -> None:
        self._print("WARNING", message)

    def ERROR(self, message : str) -> None:
        self._print("ERROR", message)

    def _print(self, log_level : str, message : str) -> None:
        print(f"{self._app_name} | {self._function_name} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} | {log_level} | {message}")
