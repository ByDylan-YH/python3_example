from math import ceil;

lst=[1,2,3,4,5];
print(list(range(0, ceil(len(lst) / 2))));

ret = [];
print(ret);
ret.extend('2');
print(ret);
ret.extend([3]);
print(ret);
ret.append(22);
print(ret);
ret.append([99]);
print(ret);