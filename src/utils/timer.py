import time


class Timer:
    __start_time: float
    __end_time: float
    __elapsed_time: float

    def __init__(self) -> None:
        self.start_time: float = 0
        self.end_time: float = 0
        self.elapsed_time: float = 0

    @property
    def start_time(self) -> float:
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time: float) -> None:
        self.__start_time = start_time

    @property
    def end_time(self) -> float:
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time: float) -> None:
        self.__end_time = end_time

    @property
    def elapsed_time(self) -> float:
        return self.__elapsed_time

    @elapsed_time.setter
    def elapsed_time(self, elapsed_time: float) -> None:
        self.__elapsed_time = elapsed_time

    def start(self) -> None:
        self.start_time = time.time()

    def end(self) -> None:
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    @property
    def get_elapsed_time(self) -> float:
        return self.elapsed_time

    @property
    def get_elapsed_time_in_ms(self) -> float:
        return self.elapsed_time * 1000

    @property
    def get_elapsed_time_in_us(self) -> float:
        return self.elapsed_time * 1000000

    @property
    def get_elapsed_time_in_ns(self) -> float:
        return self.elapsed_time * 1000000000

    @property
    def get_elapsed_time_in_ps(self) -> float:
        return self.elapsed_time * 1000000000000
