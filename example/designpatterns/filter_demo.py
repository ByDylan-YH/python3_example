class Event:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name

# 核心类
class Widget:
    # 注意 parent=None 表明默认继承关系为空
    def __init__(self, parent=None):
        self.parent = parent
    # Widget 与 Event 仅是关联关系，表明 Widget 类知道 Event 类，但对其没有严格的引用，只需要作为参数传递即可
    def handle(self, event):
        handler = 'handle_{}'.format(event)
        if hasattr(self, handler):
            method = getattr(self, handler)
            method(event)
        elif self.parent:
            self.parent.handle(event)
        elif hasattr(self, 'handle_default'):
            self.handle_default(event)

# 具有不同行为的控件 1
class MainWindow(Widget):
    def handle_close(self, event):
        print('MainWindow: {}'.format(event))
    def handle_default(self, event):
        print('MainWindow Default: {}'.format(event))

# 具有不同行为的控件 2
class SendDialog(Widget):
    def handle_paint(self, event):
        print('SendDialog: {}'.format(event))

# 具有不同行为的控件 3
class MsgText(Widget):
    def handle_down(self, event):
        print('MsgText: {}'.format(event))


def main():
    mw = MainWindow()
    sd = SendDialog(mw)
    msg = MsgText(sd)

    for e in ('down', 'paint', 'unhandled', 'close'):
        evt = Event(e)
        print('\nSending event -{}- to MainWindow'.format(evt))
        mw.handle(evt)
        print('Sending event -{}- to SendDialog'.format(evt))
        sd.handle(evt)
        print('Sending event -{}- to MsgText'.format(evt))
        msg.handle(evt)

if __name__ == '__main__':
    main()