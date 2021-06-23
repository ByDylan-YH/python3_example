# coding=utf-8
from collections import namedtuple;


class OnlineShop(object):
    def __init__(self, buidler):
        Macbook = namedtuple('Macbook', 'cpu memory ssd graphics');
        self.macbook = Macbook(buidler.cpu, buidler.memory,
                               buidler.ssd, buidler.graphics);

    def __str__(self):
        return str(self.macbook)

    class MacbookBuilder(object):
        def __init__(self):
            self.cpu = '2.7GHz';
            self.memory = '16G';
            self.ssd = '512GB';
            self.graphics = 'Radeon Pro 455';

        def upgrade_cpu(self, cpu):
            self.cpu = cpu;
            return self;

        def upgrade_memory(self, memory):
            raise ValueError('{0} is max'.format(self.memory));

        def upgrade_ssd(self, ssd):
            self.ssd = ssd;
            return self;

        def upgrade_graphics(self, graphics):
            self.graphics = graphics;
            return self;

        def builder(self):
            return OnlineShop(self);


if __name__ == '__main__':
    macbook = OnlineShop.MacbookBuilder().upgrade_cpu('2.9GHz').upgrade_ssd('2TB').upgrade_graphics('Radeon Pro 460').builder();
    print(macbook);
