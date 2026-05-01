from carDatabase import CarDatabase
from carApplication import CarApplication
from carUserInterface import CarUserInterface

# MACRO
FILE = 'car details v4.csv'

def main():
    # Layer setup
    db = CarDatabase()
    app = CarApplication(db)
    ui = CarUserInterface(app)

    ui.clearSys()

    # Fill database with data
    data = ui.runDataImport(FILE)
    ui.runFillData(data)
    ui.menu()

if __name__ == "__main__":
    main()
