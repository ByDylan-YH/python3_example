from copy import copy


class Mail:
    __receiver = ''  # 接收方
    __subject = ''  # 邮件主题
    __content = ''  # 邮件内容

    def __init__(self, receiver):
        self.__receiver = receiver

    def get_receiver(self):
        return self.__receiver

    def set_receiver(self, receiver):
        self.__receiver = receiver

    def get_subject(self):
        return self.__subject

    def set_subject(self, subject):
        self.__subject = subject

    def get_content(self):
        return self.__content

    def set_content(self, content):
        self.__content = content


# 邀请人（发送邮件的人）
class Sender:
    __receivers = ()  # 要邀请的人

    def __init__(self, receivers):
        self.__receivers = receivers

    # 发送邮件
    def send_mail(self):
        __mail = Mail('nobody')  # 定义原型
        __mail.set_subject('周末聚会')
        __mail.set_content('Hi！Guys。 周六来我家吃大虾')

        for receiver in self.__receivers:
            mail = copy(__mail)  # 使用python提供的复制对象方法
            mail.set_receiver(receiver)
            print('发送给【' + mail.get_receiver() + '】邮件【' + mail.get_subject() + '】，内容为：【' + mail.get_content() + '】')


if __name__ == '__main__':
    sender = Sender(('刘德华', '张学友', '安吉丽娜'))
    sender.send_mail()
