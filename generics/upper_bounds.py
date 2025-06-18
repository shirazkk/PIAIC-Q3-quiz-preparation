from typing import TypeVar


class Animal: ...

class Dog(Animal): ...
class Cat(Animal): ...

class Fish(): ...


AnimalType = TypeVar('AnimalType', bound=Animal)

def get_animal(animal: AnimalType) -> AnimalType:
    return animal

get_animal(Dog())  # Returns Dog instance
get_animal(Cat())  # Returns Cat instance
# get_animal(Fish())  # Raises TypeError: Fish is not a subclass of Animal