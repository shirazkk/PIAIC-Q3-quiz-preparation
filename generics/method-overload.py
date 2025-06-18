from typing import overload, Union

@overload
def add(x: int, y: int) -> int: ...
@overload
def add(x: float, y: float) -> float: ...
@overload
def add(x: str, y: str) -> str: ...

def add(x: int| str| float, y:int| str| float ):
    return x + y

print(add("Hello, ", "world!"))  # Returns "Hello, world!"
print(add(5, 3))                # Returns 8
print(add(2.5, 3.5))            # Returns 6.0