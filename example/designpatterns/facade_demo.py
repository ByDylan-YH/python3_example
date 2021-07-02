# 外观模式
class AlarmSensor:
    def run(self):
        print("Alarm Ring...")


class WaterSprinker:
    def run(self):
        print("Spray Water...")


class EmergencyDialer:
    def run(self):
        print("Dial 119...")


class EmergencyFacade:
    """
    外观类中封装了对子系统的操作
    """

    def __init__(self):
        self.alarm_sensor = AlarmSensor()
        self.water_sprinker = WaterSprinker()
        self.emergency_dialer = EmergencyDialer()

    def runAll(self):
        self.alarm_sensor.run()
        self.water_sprinker.run()
        self.emergency_dialer.run()


if __name__ == "__main__":
    emergency_facade = EmergencyFacade()
    emergency_facade.runAll()
