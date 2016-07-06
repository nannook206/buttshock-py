class ButtshockError(Exception):
    """
    General exception class for ET312 errors
    """
    pass


class ButtshockChecksumError(ButtshockError):
    pass


class ButtshockIOError(ButtshockError):
    pass

