from abc import abstractmethod

# 定义用户接口，A和B服务都引用此接口
class UserService:
    @abstractmethod
    def get_info(self, uid):
        pass

# 用户接口的实现，在B服务中
class UserServiceImpl(UserService):
    def get_info(self, uid):
        if uid == 1:
            return '张三'
        elif uid == 2:
            return '李四'
        elif uid == 3:
            return '王二'
        else:
            return None

# A服务不能直接调用B服务的方法，但是又想像使用本地方法一样调远程方法，所以增加了一层代理类
class UserServiceProxy(UserService):
    def __init__(self):
        # 这里应该是远程实现的，简单起见就直接new了
        self.userService = UserServiceImpl()
        print('我已经远程连接到了B服务')

    def get_info(self, uid):
        return self.userService.get_info(uid)


# A服务调用示例
if __name__ == '__main__':
    proxy = UserServiceProxy()
    print(proxy.get_info(2))
    print(proxy.get_info(5))