# coding=utf-8
import abc


class Receiver(object):
    '''
    命令接收者,正在执行命令的地方,实现了众多命令函数
    '''

    def start(self):
        print('execute start command')

    def stop(self):
        print('execute stop command')

    def suspend(self):
        print('execute suspend command')

    def play(self):
        print('execute play command')


class Command(object):
    """
    command抽象方法,子类必须要实现execute方法
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self):
        pass


class StartCommand(Command):
    """
    start命令类,对命令接收者类中start方法的封装
    """

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.start()


class StopCommand(Command):
    """
    stop命令类,对命令接收者类中stop方法的封装
    """

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.stop()


class Client(object):
    """
    调用命令的客户端
    """

    def __init__(self, command):
        self.command = command

    def command_do(self):
        self.command.execute()


if __name__ == '__main__':
    receiver = Receiver()
    start_command = StartCommand(receiver)
    client = Client(start_command)
    client.command_do()
    # 可以直接更换命令,如下,把start命令,换成stop命令
    stop_command = StopCommand(receiver)
    client.command = stop_command
    client.command_do()
