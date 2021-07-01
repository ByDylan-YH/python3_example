import time;

def timer(func):
    def wrapper(*args, **kwds):
        t0 = time.time();
        func(*args, **kwds);
        t1 = time.time();
        print('耗时%0.3f' % (t1 - t0,));
    return wrapper;

# timer() 是定义的装饰器函数,使用@把它附加在任何一个函数(比如do_something)定义之前,就等于把新定义的函数,当成了装饰器函数的输入参数
# 运行 do_something() 函数,可以理解为执行了timer(do_something)
@timer
def do_something(delay):
    print('函数do_something开始');
    time.sleep(delay);
    print('函数do_something结束');


do_something(1);
