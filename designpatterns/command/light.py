# 1.创建一盏灯
class Light(object):
    #可以初始化灯的类型，例如是厨房的灯还是起居室的灯
    def __init__(self, type):
        self.light = type;
    #灯本身的控制方法，on和off，这里的on和off不同于遥控器的，这只是灯自己的方法，就像是洗衣机的
    #甩干和漂洗一样
    def on(self):
        print(str(self.light) + " light On");
    def off(self):
        print(str(self.light) + " light Off");

# 2.创建遥控器
class RemoteController(object):
    def __init__(self):
        self.onCommand = {};
        self.offCommand = {};
    #这里是对遥控器的插槽和按钮进行定义
    def setCommand(self, slot, onCommand, offCommand):
        self.onCommand.setdefault(slot, onCommand);
        self.offCommand.setdefault(slot, offCommand);
    #遥控器ON按钮按下后执行的动作
    def onButtonWasPress(self, slot):
        self.onCommand[slot].execute();
    #遥控器OFF按钮按下后执行的动作
    def offButtonWasPress(self, slot):
        self.offCommand[slot].execute();

# 3.命令对象，也就是这个中间件
#电灯开
class LightOnCommand(Light):
    #传入某个电灯对象
    def __init__(self, light):
        self.light = light;
    #定义一个execute方法，调用传入对象的特定方法
    def execute(self):
        self.light.on();
#电灯关
class LightOffCommand(Light):
    def __init__(self, light):
        self.light = light;
    def execute(self):
        self.light.off();

# 4.测试一下
def client():
    controller = RemoteController();
    #要控制起居室的灯
    livingRoomLight = Light("Living Room");
    #将livingRoomLight对象传到这个中间件里面，这时这个中间件就和电灯关联了
    livingRoomLightOn = LightOnCommand(livingRoomLight);
    livingRoomLightOff = LightOffCommand(livingRoomLight);
    #定义一下遥控器的设置，0号槽控制电灯，on按钮是打开起居室的灯，off按钮是关闭起居室的灯
    #这时这个中间件又和遥控器关联了
    controller.setCommand(0, livingRoomLightOn, livingRoomLightOff);
    #控制一下
    controller.onButtonWasPress(0);
    controller.offButtonWasPress(0);
if __name__ == '__main__':
    client();
# coding=utf-8