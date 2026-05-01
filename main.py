import os
from carDatabase import CarDatabase
from carApplication import CarApplication
from carUserInterface import CarUserInterface

FILE = 'car details v4.csv'

def main():
    # Layer setup
    db = CarDatabase()
    app = CarApplication(db)
    ui = CarUserInterface(app)

    ui.clearSys()

    if app.isAlreadyLoaded():
        print("Database is loaded")
    else:
        # Check for the data
        if not os.path.exists(FILE):
            print(f"Database was found empty and the {FILE} file was not found."
            "\nDownload from https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho"
            "\nPlace within the same folder as this file and run again.")
            return

        # Fill data
        data = ui.runDataImport(FILE)
        ui.runFillData(data)

    ui.menu()

if __name__ == "__main__":
    main()
