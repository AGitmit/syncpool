class IllegalProcessAccessError(BaseException):
    def __init__(self, owner: int, accessed_by: int) -> None:
        message = f"Process #{accessed_by} tried to access the pool; The pool is only to be shared within the owner process #{owner}!"
        super().__init__(message)


class PoolClosedError(BaseException):
    def __init__(self) -> None:
        super().__init__(
            "Pool has been closed. Either re-open the pool or create a new one."
        )
