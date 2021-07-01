class Student(object):

    def __init__(self, name):
        self.name = name
        self.x, self.y = 0, 1  # 初始化两个计数器a，b

    def __str__(self):
        return 'Student object (name: %s)' % self.name

    def __call__(self):
        print('My name is %s.' % self.name)

    __slots__ = ('x', 'y', 'name', 'score', 'age')  # 用tuple定义允许绑定的属性名称

    def __getattr__(self, attr):
        if attr == 'score':
            return 99
        if attr == 'age':
            return lambda: 25
        raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)

    def __getitem__(self, n):
        if isinstance(n, int):
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice):
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L

    def __iter__(self):
        return self  # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.x, self.y = self.y, self.x + self.y  # 计算下一个值
        if self.x > 10:  # 退出循环的条件
            raise StopIteration();
        return self.x  # 返回下一个值


print("attr 方法")
s = Student('Michael')
print(s.name)
print(s.score)
print(s.age())
# AttributeError: 'Student' object has no attribute 'grade'
# print(s.grade)

print("str 方法")
print(s)

print("item 方法")
print(s[5])
print(s[0:5])
print(s[:10])

print("next,iter 方法")
for n in s:
    print(n)
