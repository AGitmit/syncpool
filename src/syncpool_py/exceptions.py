class IllegalProcessAccessError(BaseException):
    def __init__(self, owner: int, accessed_by: int) -> None:
        err_msg = f"Process #{accessed_by} tried to access the pool; The pool is only to be shared within the owner process #{owner}!"
        super().__init__(err_msg)


class PoolClosedError(BaseException):
    def __init__(self) -> None:
        err_msg = "Pool has been closed. Either re-open the pool or create a new one."
        super().__init__(err_msg)


class PoolCapacityReachedError(BaseException):
    def __init__(self) -> None:
        err_msg = "Pool is fully occupied, failed to accept passed object."
        super().__init__(err_msg)
