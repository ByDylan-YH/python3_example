from operator import itemgetter

# list 排序
L = ['bob', 'about', 'Zoo', 'Credit']
print(sorted(L))
print(sorted(L, key=str.lower))
students = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
print(sorted(students, key=itemgetter(0)))
print(sorted(students, key=lambda t: t[1]))
print(sorted(students, key=itemgetter(1), reverse=True))


# list过滤
def is_odd(n):
    return n % 2 == 1

L = range(100)

print(list(filter(is_odd, L)))

# 对 list 施加函数操作
def f(x):
    return x * x

print(list(map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])))


# list 提取
L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']

print('L[0:3] =', L[0:3])
print('L[:3] =', L[:3])
print('L[1:3] =', L[1:3])
print('L[-2:] =', L[-2:])

R = list(range(100))
print('R[:10] =', R[:10])
print('R[-10:] =', R[-10:])
print('R[10:20] =', R[10:20])
print('R[:10:2] =', R[:10:2])
print('R[::5] =', R[::5])

# list 遍历
print([x * x for x in range(1, 11)])
print([x * x for x in range(1, 11) if x % 2 == 0])
# 牛逼 plus
print([m + n for m in 'ABC' for n in 'XYZ'])

d = {'x': 'A', 'y': 'B', 'z': 'C' }
print([k + '=' + v for k, v in d.items()])

L = ['Hello', 'World', 'IBM', 'Apple']
print([s.lower() for s in L])