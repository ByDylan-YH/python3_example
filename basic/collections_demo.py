from collections import deque
from collections import Counter
from collections import namedtuple
from collections import defaultdict

# 坐标点
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print('Point:', p.x, p.y)

# 高度相似于java list
q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)

# 带默认值的 dict
dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'abc'
print('dd[\'key1\'] =', dd['key1'])
print('dd[\'key2\'] =', dd['key2'])

# 返回统计的 dict
c = Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1
print(c)
