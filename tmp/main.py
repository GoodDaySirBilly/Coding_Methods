from abc import ABC, abstractmethod

class BaseClass(ABC):

    def __init__(self):
        self.__z = 1

    @property
    @abstractmethod
    def required_field(self):
        """This property must be implemented by subclasses."""
        pass

    @property
    def z(self): return self.__z

class ConcreteClass(BaseClass):
    def __init__(self, value):
        super().__init__()
        self._required_field = value

    @property
    def required_field(self):
        return self._required_field

# This would raise a TypeError because required_field is not implemented
# invalid_instance = BaseClass() 

# This works because ConcreteClass implements required_field
instance = ConcreteClass("Hello")
print(instance.required_field)
print(instance.z)