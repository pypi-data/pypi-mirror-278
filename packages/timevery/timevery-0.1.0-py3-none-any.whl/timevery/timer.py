import time
from contextlib import ContextDecorator
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional, Union


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class."""


@dataclass
class TimeRecord:
    total_time: float = 0
    time: List[float] = field(default_factory=list)


@dataclass
class Timer(ContextDecorator):
    name: str = "Timer"
    text: str = "Elapsed time of {name}: {seconds:0.4f} seconds. "
    initial_text: Union[bool, str] = False
    show_freq: bool = False
    show_report: bool = False
    auto_restart: bool = False
    logger: Callable = print

    def __init__(
        self,
        name: Optional[str] = "Timer",
        text: Optional[str] = "Elapsed time of {name}: {seconds:0.4f} seconds. ",
        initial_text: Union[bool, str] = False,
        show_freq: Optional[bool] = False,
        show_report: Optional[bool] = False,
        auto_restart: Optional[bool] = False,
        logger: Optional[Callable] = print,
        time_function: Optional[Callable] = time.perf_counter,
    ):
        """Create a Timer.

        Args:
            name (Optional[str], optional): Timer's name. Defaults to "Timer".
            text (Optional[str]): Then text shown when `stop()` or `lap()` is called.
                Defaults to "Elapsed time of {name}: {seconds:0.4f} seconds. ".
                Available substitutions: {name}, {milliseconds}, {seconds}, {minutes}.
            initial_text (Union[bool, str], optional): The text shown when `start()` is called. Defaults to False.
            show_freq (Optional[str]): Show frequency when `stop()` is called if is True. Defaults to False.
            show_report (Optional[str]): Show report when `stop()` is called if is True. Defaults to False.
            auto_restart: Optional[bool]: Restart the timer when `start()` is called if is True. Defaults to False.
            logger (Optional[Callable], optional): Callable to show logs. Defaults to `print`.
            time_function (Optional[Callable], optional): The function can return a number to indicate the time it be called.
                Defaults to `time.perf_counter()` in seconds. `time.time()`, `time.monotonic()`, `time.process_time()` are also available.
        """

        self.name = name
        self.text = text
        if isinstance(initial_text, bool):
            if initial_text:
                initial_text = "{name} started."
        elif not isinstance(initial_text, str):
            raise TimerError("initial_text must be a string or a boolean.")
        self.initial_text = initial_text
        self.show_freq = show_freq
        self.show_report = show_report
        self.auto_restart = auto_restart
        self.logger = logger
        self.time_function = time_function  # get a time in seconds
        self._records = {name: TimeRecord()}
        self._start_time = None
        self._lap_start_time = None

    def start(self):
        """Start a new timer."""
        if self._start_time is not None:
            if self.auto_restart:
                self.lap("auto-restart")
                self.stop()
            else:
                raise TimerError("Timer is running. Use .stop() to stop it")

        # Log initial text when timer starts
        if self.logger and self.initial_text:
            initial_text = self.initial_text.format(name=self.name)
            self.logger(initial_text)

        self._start_time = self.time_function()
        self._lap_start_time = self._start_time

    def lap(self, name: Optional[str] = None) -> float:
        """Record a lap time."""
        if name is None:
            name = str(len(self._records))
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        elapsed_time = self.time_function() - self._lap_start_time
        self._update_record(name, elapsed_time)
        self._lap_start_time = self.time_function()

        if self.logger:
            attributes = {
                "name": name,
                "milliseconds": elapsed_time * 1000,
                "seconds": elapsed_time,
                "minutes": elapsed_time / 60,
            }
            text = self.text.format(**attributes)
            self.logger(str(text))

        return elapsed_time

    def stop(
        self,
    ) -> float:
        """Stop the timer, and report the elapsed time."""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        elapsed_time = self.time_function() - self._start_time
        self._update_record(self.name, elapsed_time)
        self._start_time = None
        self._lap_start_time = None

        # Report elapsed time
        if self.logger:
            attributes = {
                "name": self.name,
                "milliseconds": elapsed_time * 1000,
                "seconds": elapsed_time,
                "minutes": elapsed_time / 60,
            }
            text = self.text.format(**attributes)

            if self.show_freq:
                freq = 1 / elapsed_time
                freq_text = f" Frequency: {freq:.2f} Hz"
                text += freq_text

            self.logger(str(text))
        if self.show_report:
            self.report()
        return elapsed_time

    def report(self):
        from rich import box
        from rich.console import Console
        from rich.table import Table

        c = Console()

        headers = [
            "Name",
            "Total(s)",
            "Average(s)",
            "Freq(Hz)",
            "Percent(%)",
            "Count",
            "Min",
            "Max",
        ]
        t = Table(show_header=True, header_style="bold magenta", box=box.MARKDOWN)
        for header in headers:
            t.add_column(header, justify="center")

        total_time = self._records[self.name].total_time
        for name, record in self._records.items():
            total = record.total_time
            average = total / len(record.time)
            freq = 1 / average
            percent = total / total_time * 100
            count = len(record.time)
            min_time = min(record.time)
            max_time = max(record.time)

            t.add_row(
                name,
                f"{total:.4f}",
                f"{average:.4f}",
                f"{freq:.4f}",
                f"{percent:.4f}",
                f"{count}",
                f"{min_time:.4f}",
                f"{max_time:.4f}",
            )
        c.print(t)

    def _update_record(self, name: str, time: float):
        if name not in self._records:
            self._records[name] = TimeRecord()
        self._records[name].time.append(time)
        self._records[name].total_time += time

    def __enter__(self) -> "Timer":
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.stop()
