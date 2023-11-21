from asyncio import Lock
from os import stat, rename, listdir, remove
from time import gmtime

from logging.appender.base import Appender
from logging.encoder.encoder import Encoder
from logging.log_event import LogEvent


class FileAppender(Appender):
    def __init__(self, name: str, encoder: Encoder,
                 file_path: str = "application.log",
                 rollover_size: int = 25600,
                 rolling_file_count: int = 4):
        super().__init__(name, encoder)
        self.file_path = file_path
        self.file_directory = "/".join(self.file_path.split("/")[0:-1])
        self.file_name = self.file_path.split("/")[-1]
        self.rollover_size = rollover_size
        self.rolling_file_count = rolling_file_count
        self.current_size = 0
        self._file_lock: Lock = Lock()

    def __str__(self):
        return f"FileAppender('{self.name}', {self.encoder}, file_path='{self.file_path}')"

    async def write(self, event: LogEvent):
        await self.write_line_to_file(event)  # todo open/close on every write?
        await self.update_file_size()
        if self.current_size > self.rollover_size:
            await self.rollover_file()
        await self.cleanup_old_files()

    async def write_line_to_file(self, event: LogEvent):
        async with self._file_lock:
            with open(self.file_path, "a") as output:
                try:
                    output.write(self.encoder.encode(event))
                    output.write("\n")
                except OSError as error:
                    if error.errno == 28:  # ENOSPC No space left on device
                        print("Unable to write to log file, no space left")
                    else:
                        raise error

    async def update_file_size(self):
        # mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime = stat(self.file_path)
        _, _, _, _, _, _, size, _, _, _ = stat(self.file_path)
        self.current_size = size

    async def rollover_file(self):
        async with self._file_lock:
            year, month, day, hour, minute, second, _, _ = gmtime()
            suffix = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(year, month, day, hour, minute, second)
            rename(self.file_path, f"{self.file_path}.{suffix}")

    async def cleanup_old_files(self):
        existing_log_files = []
        for filename in listdir(self.file_directory):
            if filename.startswith(self.file_name):
                existing_log_files.append(filename)
        existing_log_files.sort(key=lambda it: stat(it)[8])
        while len(existing_log_files) > self.rolling_file_count:
            filename = existing_log_files.pop(0)
            print(f"Removing log file = {filename})")
            remove(filename)
