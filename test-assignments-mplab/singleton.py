'''
Fix code:

class SingletonMeta(type):

    _instances = {}

    def str(cls, *args, **kwargs):
        if cls in cls._instances:
            instance = super().call(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
'''


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# class Foo(metaclass = SingletonMeta):
#     counter = 0
#     def say(self):
#         self.counter += 1
#         print(f'Konichiwa, za Warudo! Time stops for {self.counter} seconds!')

# something = Foo()
# another_one = Foo()


# something.say()
# another_one.say()


# $python3 singleton.py
# Output:
#     Konichiwa, za Warudo! Time stops for 1 seconds!
#     Konichiwa, za Warudo! Time stops for 2 seconds!


