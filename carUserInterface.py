import os
from flask import Flask, request, jsonify, render_template
from carDatabase import CarDatabase
from carApplication import CarApplication
from carClasses import Car, Cost, Appearance, Performance, Specs

FILE = 'car details v4.csv'

FILTER_MAP = {
    "make": "cr.make",
    "model": "cr.model",
    "year": "cr.year",
    "price": "cst.price",
    "location": "cst.location",
    "owner": "cst.owner",
    "seller": "cst.seller",
    "color": "app.color",
    "length": "app.length",
    "width": "app.width",
    "height": "app.height",
    "seats": "app.seats",
    "tank_size": "app.tank_size",
    "fuel_type": "perf.fuel_type",
    "transmission": "perf.transmission",
    "kilometers_driven": "perf.kilometers_driven",
    "drivetrain": "spc.drivetrain",
    "engine": "spc.engine",
    "max_power": "spc.max_power",
    "max_torque": "spc.max_torque",
}

# Layer definitions
app = Flask(__name__)
db  = CarDatabase()
ap  = CarApplication(db)

def main():
    loadIfNeeded()
    app.run(debug=True)

# Startup database loading
def loadIfNeeded():
    if ap.isAlreadyLoaded():
        print("Database is loaded")
    else:
        # Check for the data
        if not os.path.exists(FILE):
            print(f"Database was found empty and the {FILE} file was not found."
            "\nDownload from https://www.kaggle.com/datasets/nehalbirla/vehicle-dataset-from-cardekho"
            "\nPlace within the same folder as this file and run again.")
            return


        print("Seeding database from CSV...")
        data = ap.dataImport(CSV_FILE)
        ap.fillDatabase(data, lambda p, t: print(f" {p}/{t} cars imported", end="\r"), len(data))
        print("\nDatabase ready.")

# Route for the main UI
@app.route("/")
def index():
    return render_template("frontend.html")

# Route to filters for car
@app.route("/api/cars", methods=["GET"])
def filterCars():
    filters = []
 
    for param, col in FILTER_MAP.items():
        value = request.args.get(param)
        if value is None:
            continue
        try:
            # First try to make an int
            converted = int(value)
        except ValueError:
            try:
                # Then backup to a float answer
                converted = float(value)
            except ValueError:
                # completely wrong input found
                converted = value
 
        filters.append((col, converted))
 
    if not filters:
        return jsonify({"error": "Provide at least one filter parameter."}), 400
 
    rows = ap.getFilteredCars(filters)
    cars = []
    for r in rows:
        cars.append({"car_id": r[0], "year": r[1], "make": r[2], "model": r[3]})
    

    return jsonify(cars)

# Route to filter by car id
@app.route("/api/cars/<int:car_id>", methods=["GET"])
def getCarById(car_id):
    car = ap.getCar(car_id)
    if car is None:
        return jsonify({"error": f"No car found with id {car_id}."}), 404
 
    keys = [
        "car_id", "make", "model", "year",
        "price", "location", "owner", "seller",
        "color", "length", "width", "height", "seats", "tank_size",
        "fuel_type", "transmission", "kilometers_driven",
        "drivetrain", "engine", "max_power", "max_torque",
    ]
    return jsonify(dict(zip(keys, car)))

# Route to add a car
@app.route("/api/cars", methods=["POST"])
def addANewCar():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Request body must be JSON."}), 400
 
    # Required parts of the car
    for field in ("make", "model", "year"):
        if field not in body:
            return jsonify({"error": f"Missing required field: '{field}'."}), 400
 
    try:
        year = int(body["year"])
    except (ValueError, TypeError):
        return jsonify({"error": "'year' must be an integer."}), 400
 
    car = Car(
        body["make"], 
        body["model"], 
        year
    )

    cost = Cost(
        body.get("price", 0),
        body.get("location", "NA"),
        body.get("owner", "NA"),
        body.get("seller", "NA"),
    )

    appear = Appearance(
        body.get("color", "NA"),
        body.get("length", 0),
        body.get("width", 0),
        body.get("height", 0),
        body.get("seats", 0),
        body.get("tank_size", 0),
    )

    perf = Performance(
        body.get("fuel_type", "NA"),
        body.get("transmission", "NA"),
        body.get("kilometers_driven", 0),
    )

    specs = Specs(
        body.get("drivetrain", "NA"),
        body.get("engine", "NA"),
        body.get("max_power", "NA"),
        body.get("max_torque", "NA"),
    )
 
    ap.sendCarToDb(car, cost, appear, perf, specs)
    return jsonify({"message": "Car added successfully."}), 201
 
if __name__ == "__main__":
    main()