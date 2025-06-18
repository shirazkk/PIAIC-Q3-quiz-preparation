

class Cashe[K,V]:
    def __init__(self):
        self.store: dict[K,V] = {}


    def set(self, Key:K, Value: V)-> None:
        self.store[Key] = Value


    def get(self, Key: K) -> V:
        return self.store[Key]
    


cashe = Cashe[str, int]()

cashe.set("one", 1)
cashe.set("two", 2)

print(cashe.get("one"))  # Returns 1
print(cashe.get("two"))  # Returns 2