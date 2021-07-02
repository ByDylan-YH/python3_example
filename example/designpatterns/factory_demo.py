import abc


class Mercedes(object):
    def __repr__(self):
        return "Mercedes-Benz"


class BMW(object):
    def __repr__(self):
        return "BMW"


class AbstractFactory(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def product_car(self):
        pass


class MercedesFactory(AbstractFactory):
    def product_car(self):
        return Mercedes()


class BMWFactory(AbstractFactory):
    def product_car(self):
        return BMW()


if __name__ == '__main__':
    print(MercedesFactory().product_car())
    print(BMWFactory().product_car())
