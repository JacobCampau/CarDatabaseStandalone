import pandas as pd
from carClasses import Car, Cost, Appearance, Performance, Specs
from carDatabase import CarDatabase

class CarApplication:
    def __init__(self, db):
        self.db = db

    def getCar(self, car_id):
        return self.db.getCarDetails(car_id)
    
    # Data import

    def dataImport(self, file):
        data = pd.read_csv(file)

        # fills the empty columns with "NA"
        data = data.fillna("NA")

        # cleaning numeric columns and fill empty ones with -1
        numeric_cols = ["Price", "Kilometer", "Length", "Width", "Height", "Seating Capacity", "Fuel Tank Capacity"]
        for col in numeric_cols:
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
            cst = Cost(row["Price"], row["Location"], row["Owner"], row["Seller Type"])
            appear = Appearance(row["Color"], row["Length"], row["Width"], row["Height"], row["Seating Capacity"], row["Fuel Tank Capacity"])
            perf = Performance(row["Fuel Type"], row["Transmission"], row["Kilometer"])
            spc = Specs(row["Drivetrain"], row["Engine"], row["Max Power"], row["Max Torque"])

            self.db.importFullCar(cr, cst, appear, perf, spc)

            progressTracker(tracker, tot)
        
        self.db.endDbConn()
    
    def isAlreadyLoaded(self):
        # Returns true if the database is filled with something
        return self.db.isLoaded()

    def getFilteredCars(self, filter_list):
        return self.db.executeFilters(filter_list)

    def sendCarToDb(self, car, cost, appear, perf, specs):
        self.db.startDbConn()
        self.db.importFullCar(car, cost, appear, perf, specs)
        self.db.endDbConn()