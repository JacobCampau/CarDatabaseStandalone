class Car:
    def __init__(self, make, model, year, carId = None):
        self.make = make
        self.model = model
        self.year = year
        self.carId = carId

class Cost:
    def __init__(self, price, loc, own, sellType, carId = None):
        self.price = price
        self.loc = loc
        self.own = own
        self.sellType = sellType
        self.carId = carId

class Appearance:
    def __init__(self, color, length, width, height, seatNum, tank, carId = None):
        self.color = color
        self.length = length
        self.width = width
        self.height = height
        self.seatNum = seatNum
        self.tank = tank
        self.carId = carId

class Performance:
    def __init__(self, fuel, trans, kilo, carId = None):
        self.fuel = fuel
        self.trans = trans
        self.kilo = kilo
        self.carId = carId

class Specs:
    def __init__(self, driveTrain, engine, maxPow, maxTor, carId = None):
        self.driveTrain = driveTrain
        self.engine = engine
        self.maxPow = maxPow
        self.maxTor = maxTor
        self.carId = carId