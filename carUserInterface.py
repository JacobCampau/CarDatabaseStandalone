import os
from tqdm import tqdm
from tabulate import tabulate
from carDatabase import CarDatabase
from carApplication import CarApplication
from carClasses import Car
from carClasses import Cost
from carClasses import Appearance
from carClasses import Performance
from carClasses import Specs

# MACRO
FILTERS = {
    1: ("cr.make", str),
    2: ("cr.model", str),
    3: ("cr.year", int),
    4: ("cst.price", float),
    5: ("cst.location", str),
    6: ("cst.owner", int),
    7: ("cst.seller", str),
    8: ("app.color", str),
    9: ("app.length", float),
    10: ("app.width", float),
    11: ("app.height", float),
    12: ("app.seats", int),
    13: ("app.tank_size", float),
    14: ("perf.fuel_type", str),
    15: ("perf.transmission", str),
    16: ("perf.kilometers_driven", float),
    17: ("spc.drivetrain", str),
    18: ("spc.engine", str),
    19: ("spc.max_power", str),
    20: ("spc.max_torque", str)
}

class CarUserInterface:
    def __init__(self, ap):
        self.ap = ap
        
    def clearSys(self):
        if(os.name == 'nt'):
            os.system('cls')
        else:
            os.system('clear')

    def runDataImport(self, filePath):
        print("Data import beginning...")
        return self.ap.dataImport(filePath)

    def runFillData(self, data):
        rowNum = len(data)

        with tqdm(total=rowNum, desc="Importing Cars", unit="Car") as bar:
            def progress(progress, total):
                bar.n  = progress
                bar.refresh()

            self.ap.fillDatabase(data, progress, rowNum)    
        
        print("\nDatabase filled. Welcome to 'Car Search'\n")

    def getIntInput(self, lower, upper, message):
        while True:
            choice = input(message)

            try:
                choiceInt = int(choice)
            except ValueError:
                print("Not a valid input. Give a number.")
                continue

            if lower <= choiceInt and choiceInt <= upper:
                return choiceInt
            else:
                print("Not a valid input. Try again.")

    def menu(self):
        while True:
            print("___Menu Screen___")
            print("Select an option:")
            print("1. Filter search")
            print("2. Add Car")
            print("3. View Car by id")
            print("0. Exit program")

            menChoice = self.getIntInput(0,3,"\nEnter a number: ")

            if menChoice == 1:
                self.filterMenu()
            elif menChoice == 2:
                self.addCarMenu()
            elif menChoice == 3:
                self.viewCarMenu()
            else:
                print("\nClosing program...")
                break

    # filter search a list of cars

    def filterMenu(self):
        self.clearSys()

        print("___Filter Menu___")
        print("Choose filters one at a time by their filter number (#)")
        print("(01)Make        (02)Model        (03)Year          (04)Price")
        print("(05)Location    (06)Owner Count  (07)Seller Type   (08)Color")
        print("(09)Length      (10)Width        (11)Height        (12)Seat Count")
        print("(13)Tank Size   (14)Fuel Type    (15)Transmission  (16)Kilometers Driven")
        print("(17)Drivetrain  (18)Engine       (19)Max Power     (20)Max Torque")
        print("\n(0) Execute applied filters\n")

        filters = []

        while True:
            choice = self.getIntInput(0,20,"Enter a filter id: ")

            if choice == 0:
                break
            
            col, dataType = FILTERS[choice]
            insertedValue = input("Give a value for this filter: ")

            try:
                convertedValue = dataType(insertedValue)
            except:
                print("Not a valid input. Try again.")
                continue

            filters.append((col, convertedValue))
            print(f"Added filter for {col} = {convertedValue}")

        if len(filters) == 0:
            input("\nNo filters given, press enter to return to main menu")
            self.clearSys()
        else:
            self.clearSys()
            print("Filters applied: ")
            results = self.ap.getFilteredCars(filters)

            headers = ["Car ID", "Year", "Make", "Model"]
            print(tabulate(results, headers=headers, tablefmt="fancy_grid"))

            input("\nPress 'ENTER' to return to main menu")
            self.clearSys()

    # adding custom car

    def addCarMenu(self):
        self.clearSys()

        print("___Add Car___")
        make = input("Give the make: ")
        model = input("Give the model: ")
        year = self.getIntInput(0,3000,"Give the year: ")

        tempCar = Car(make, model, year)

        # temp values to know what was added during UI print later
        tempAppear = Appearance("NA", 0, 0, 0, 0, 0)
        tempCost = Cost(0, "NA", "NA", "NA")
        tempPerf = Performance("NA", "NA", 0)
        tempSpecs = Specs("NA", "NA", "NA", "NA")

        components = {
            "Appearance": (tempAppear, self.printAppearance),
            "Cost": (tempCost, self.printCost),
            "Performance": (tempPerf, self.printPerformance),
            "Specs": (tempSpecs, self.printSpecs)
        }

        compnentList = ["Appearance", "Cost", "Performance", "Specs"]
        componentsChanged = []

        while True:
            self.clearSys()

            print(f"CAR: {year} {make} {model}\n")
            print("Now choose what components you will add information to")
            print("1. Appearance")
            print("2. Cost")
            print("3. Performance")
            print("4. Specs")
            print("0. Add no more information")

            choice = self.getIntInput(0,4,"\nEnter a choice: ")

            if choice == 0:
                self.clearSys()
                break

            componentsChanged.append(compnentList[choice-1])
            if choice == 1:
                self.fillAppear(tempAppear)
            elif choice == 2:
                self.fillCost(tempCost)
            elif choice == 3:
                self.fillPerf(tempPerf)
            else:
                self.fillSpecs(tempSpecs)

        print("___Final Car Information___")
        self.printCar(tempCar)
        
        for item in componentsChanged:
            comp, printFunc = components[item]
            printFunc(comp)

        choice = self.getIntInput(0,1, "\nSend car to database? (0 for no, 1 for yes): ")

        if choice == 1:
            self.ap.sendCarToDb(tempCar, tempCost, tempAppear, tempPerf, tempSpecs)
            print("CAR ADDED TO DATABASE...\n")
        else:
            print("CAR DISCARDED...\n")

        input("Press 'ENTER' to return to main menu")
        self.clearSys()

    # fill functions for temp car component objects

    def optionalFill(self, text, inputType, defaultVal):
        newVal = input(text)
        if newVal.strip() == "":
            return defaultVal
        
        try:
            return inputType(newVal)
        except:
            print("Invalid input, keeping the default value")
            return default

    def fillAppear(self, appear):
        print("\n___FILL APPEARANCE___ (Press 'ENTER' to skip)")
        appear.color = self.optionalFill("Color: ", str, appear.color)
        appear.length = self.optionalFill("Length: ", float, appear.length)
        appear.width = self.optionalFill("Width: ", float, appear.width)
        appear.height = self.optionalFill("Height: ", float, appear.height)
        appear.seatNum = self.optionalFill("Seat Count: ", int, appear.seatNum)
        appear.tank = self.optionalFill("Tank Size: ", float, appear.tank)

    def fillCost(self, cost):
        print("\n___FILL COST___ (Press 'ENTER' to skip)")
        cost.price = self.optionalFill("Price: ", float, cost.price)
        cost.loc = self.optionalFill("Location: ", str, cost.loc)
        cost.own = self.optionalFill("Owner Count: ", int, cost.own)
        cost.sellType = self.optionalFill("Seller Type: ", str, cost.sellType)

    def fillPerf(self, perf):
        print("\n___FILL PERFORMANCE___ (Press 'ENTER' to skip)")
        perf.fuel = self.optionalFill("Fuel Type: ", str, perf.fuel)
        perf.trans = self.optionalFill("Transmission: ", str, perf.trans)
        perf.kilo = self.optionalFill("Kilometers Driven: ", float, perf.kilo)

    def fillSpecs(self, specs):
        print("\n___FILL SPECS___ (Press 'ENTER' to skip)")
        specs.drivetrain = self.optionalFill("Drivetrain: ", str, specs.drivetrain)
        specs.engine = self.optionalFill("Engine: ", str, specs.engine)
        specs.maxPow = self.optionalFill("Max Power: ", str, specs.maxPow)
        specs.maxTor = self.optionalFill("Max Torque: ", str, specs.maxTor)

    # print functions for added cars

    def printCar(self, car):
        print(f"Basic Info: {car.year} {car.make} {car.model}")

    def printChangedValue(self, text, value, default):
        if value != default:
            print(f" > {text}: {value}")

    def printAppearance(self, appear):
        print("\nAppearance:")
        self.printChangedValue("Color", appear.color, "NA")
        self.printChangedValue("Length", appear.length, 0)
        self.printChangedValue("Width", appear.width, 0)
        self.printChangedValue("Height", appear.height, 0)
        self.printChangedValue("Seats", appear.seatNum, 0)
        self.printChangedValue("Tank Size", appear.tank, 0)
        
    def printCost(self, cost):
        print("\nCost:")
        self.printChangedValue("Price", cost.price, 0)
        self.printChangedValue("Location", cost.loc, "NA")
        self.printChangedValue("Owner Count", cost.own, "NA")
        self.printChangedValue("Seller", cost.sellType, "NA")

    def printPerformance(self, perf):
        print("\nPerformance:")
        self.printChangedValue("Fuel Type", perf.fuel, "NA")
        self.printChangedValue("Transmission", perf.trans, "NA")
        self.printChangedValue("Kilometers driven", perf.kilo, 0)

    def printSpecs(self, specs):
        print("\nSpecs:")
        self.printChangedValue("Drivetrain", specs.drivetrain, "NA")
        self.printChangedValue("Engine", specs.engine, "NA")
        self.printChangedValue("Max Power", specs.maxPow, "NA")
        self.printChangedValue("Max Torque", specs.maxTor, "NA")

    # View a car by its id menu

    def viewCarMenu(self):
        self.clearSys()

        print("___View Car___")
        carId = self.getIntInput(0,9999,"Give car id: ")

        car = self.ap.getCar(carId)

        if car is None:
            print("\nNo vehicle belongs to this id")
        else:
            self.clearSys()

            headers = [
                "Car ID","Make","Model","Year",
                "Price","Location","Owner Count","Seller",
                "Color","Length","Width","Height","Seats","Tank Size",
                "Fuel Type","Transmission","Kilo Driven",
                "Drivetrain","Engine","Max Power","Max Torque"
            ]

            print("___Vehicle Details___")
            rows = list(zip(headers, car))
            print(tabulate(rows, headers=["Attribute", "Value"], tablefmt="fancy_grid"))
        
        input("\nPress ENTER to return to main menu")

        self.clearSys()