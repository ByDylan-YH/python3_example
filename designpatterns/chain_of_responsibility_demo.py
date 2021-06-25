# coding=utf-8

# 责任链模式
# 抽象接口
class Handler:

    def __init__(self):
        pass;

    def successor(self, successor):
        self.successor = successor;

    def handle(self, request):
        pass;

# 接口实现方法handler1
class ConcreteHandler1(Handler):

    def handle(self, request):
        if 0 < request <= 10:
            print("in handler1");
        else:
            self.successor.handle(request);

# 接口实现方法handler2
class ConcreteHandler2(Handler):
    def handle(self, request):
        if 10 < request <= 20:
            print("in handler2");
        else:
            self.successor.handle(request);

# 接口实现方法handler3
class ConcreteHandler3(Handler):
    def handle(self, request):
        if 20 < request <= 30:
            print("in handler3");
        else:
            self.successor.handle(request);

# 最终处理handler
class FinalHandler(Handler):
    def handle(self, request):
        print('end of chain, no handler for {}'.format(request));

class Client(object):
    def __init__(self):
        h1 = ConcreteHandler1();
        h2 = ConcreteHandler2();
        h3 = ConcreteHandler3();
        final = FinalHandler();
        # 这里再实例化完成之后进行任务的传递过程设置
        h1.successor(h2);
        h2.successor(h3);
        h3.successor(final);

        requests = [2, 5, 14, 22, 18, 3, 35, 27, 20];
        for request in requests:
            h1.handle(request);


if __name__ == "__main__":
    client = Client();
