import csv
import pandas as pd
from carClasses import Car
from carClasses import Cost
from carClasses import Appearance
from carClasses import Performance
from carClasses import Specs
from carDatabase import CarDatabase

class CarApplication:
    def __init__(self, db):
        self.db = db

    def getCar(self, carId):
        return self.db.getCarDetails(carId)
    
    # Data import

    def dataImport(self, file):
        data = pd.read_csv(file)

        # fills the empty columns with "NA"
        data.fillna("NA")

        # cleaning numeric columns and fill empty ones with -1
        numericCols = ["Price", "Kilometer", "Length", "Width", "Height", "Seating Capacity", "Fuel Tank Capacity"]
        for col in numericCols:
            if col in data.columns:
                data[col] = (data[col].astype(str).str.extract(r"(\d+)").fillna(-1).astype(float))

        return data
    
    def fillDatabase(self, data, progressTracker, tot):
        self.db.createTables()
        self.db.startDbConn()

        tracker = 0
        for _, row in data.iterrows():
            tracker += 1

            cr = Car(row["Make"], row["Model"], row["Year"])
            cst = Cost(row["Price"], row["Location"], row["Owner"], row["Seller Type"], id)
            appear = Appearance(row["Color"], row["Length"], row["Width"], row["Height"], row["Seating Capacity"], row["Fuel Tank Capacity"], id)
            perf = Performance(row["Fuel Type"], row["Transmission"], row["Kilometer"], id)
            spc = Specs(row["Drivetrain"], row["Engine"], row["Max Power"], row["Max Torque"], id)

            self.db.importFullCar(cr, cst, appear, perf, spc)

            progressTracker(tracker, tot)
        
        self.db.endDbConn()
    
    def getFilteredCars(self, filterList):
        return self.db.executeFilters(filterList)

    def sendCarToDb(self, car, cost, appear, perf, specs):
        self.db.startDbConn()
        self.db.importFullCar(car, cost, appear, perf, specs)
        self.db.endDbConn()