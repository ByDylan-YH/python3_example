import re;

# re.match(pattern, string, flags=0)
print(re.match('www', 'www.runoob.com').span());  # 在起始位置匹配
print(re.match('com', 'www.runoob.com'));  # 不在起始位置匹配

# 实例
# re.match只匹配字符串的开始,如果字符串开始不符合正则表达式,则匹配失败,函数返回None;而re.search匹配整个字符串,直到找到一个匹配
# re.I	使匹配对大小写不敏感
# re.L	做本地化识别（locale-aware）匹配
# re.M	多行匹配，影响 ^ 和 $
# re.S	使 . 匹配包括换行在内的所有字符
# re.U	根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B
# re.X	该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解
line = "Cats are smarter than dogs";

matchObj = re.match(r'dogs', line, re.M | re.I);
if matchObj:
    print("match --> matchObj.group() : ", matchObj.group());
else:
    print("No match!!");

matchObj = re.search(r'dogs', line, re.M | re.I);
if matchObj:
    print("search --> matchObj.group() : ", matchObj.group());
else:
    print("No match!!");

# 替换操作
# re.sub(pattern, repl, string, count=0, flags=0)

# pattern : 正则中的模式字符串
# repl : 替换的字符串,也可为一个函数
# string : 要被查找替换的原始字符串
# count : 模式匹配后替换的最大次数,默认 0 表示替换所有的匹配
# flags : 编译时用的匹配模式,数字形式

phone = "2004-959-559 # 这是一个电话号码";

# 删除注释
num = re.sub(r"#.*$", "", phone);
print("电话号码 : ", num);

# 移除非数字的内容
num = re.sub(r'\D', "", phone);
print("电话号码 : ", num);


# 当 repl 为一个函数的时候
# 将匹配的数字乘于 2
def double(matched):
    value = int(matched.group('value'));
    return str(value * 2);


s = 'A23G4HFD567';
pattern = re.compile(r'(?P<value>\d+)');
print('pattern.match: ', pattern.match(s));  # 这样居然不行
print('re.search: ', re.search(r'(?P<value>\d+)', s));
print('pattern.findall: ', pattern.findall(s));  # 查找匹配到的所有子串

it = re.finditer(r"(?P<value>\d+)", s);  # 返回一个迭代器
for match in it:
    print('re.finditer: ', match.group(), end=" ");
print();
print('re.split: ', re.split(r"(?P<value>\d+)", s));  # split 方法按照能够匹配的子串将字符串分割后返回列表
print('re.sub: ', re.sub('(?P<value>\d+)', double, s));
