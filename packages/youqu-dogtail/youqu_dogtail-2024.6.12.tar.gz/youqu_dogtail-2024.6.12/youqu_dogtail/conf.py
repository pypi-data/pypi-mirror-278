import platform


class Config:
    ARCH = platform.machine()

    PASSWORD = "1"


conf = Config()
