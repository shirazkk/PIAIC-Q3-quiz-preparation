from typing import Optional

class OperationResult[T, E]:
    def __init__(self, success_data: Optional[T] = None, error_data: Optional[E] = None):
        self.success_data = success_data
        self.error_data = error_data

    def is_successful(self) -> bool:
        return self.success_data is not None

    def get_result(self) -> T:
        if self.is_successful():
            assert self.success_data is not None
            return self.success_data
        raise ValueError("No successful result")

    def get_error(self) -> E:
        if not self.is_successful():
            assert self.error_data is not None
            return self.error_data
        raise ValueError("No error occurred")

# Example Usage
result = OperationResult[int, str](error_data="An error occurred")
if result.is_successful():
    print(f"Success: {result.get_result()}")
else:
    print(f"Error: {result.get_error()}")
