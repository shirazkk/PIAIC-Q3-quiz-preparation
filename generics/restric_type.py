
from typing import TypeVar


Numeric = TypeVar('Numeric', bound=int | float)

def add(a:Numeric,b:Numeric)-> Numeric:
    return a + b



print(add(1,2))
print(add(1.2,1.2))

# print(add("Hello, ", "world!"))  # Returns "Hello, world!"