class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# 将 metaclass 指向 Singleton 类,让 Singleton 中的 type 来创造新的 Cls4 实例
class Cls4(metaclass=Singleton):
    pass


cls1 = Cls4()
cls2 = Cls4()
print(id(cls1) == id(cls2))
