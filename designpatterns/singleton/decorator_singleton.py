# coding=utf-8

# 使用装饰器
def singleton(cls):
    _instances = {};

    def getinstance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw);
        return _instances[cls];

    return getinstance;


@singleton
class MyClass(object):
    a = 1;

one = MyClass();
two = MyClass();
print(one==two);
print(one is two);