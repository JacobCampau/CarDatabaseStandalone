import sqlite3

DB_PATH = "CarInformation.db"

class CarDatabase:
    def __init__(self):
        self.db_path = DB_PATH

    def connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def createTables(self):
        create_tables = [
            "DROP TABLE IF EXISTS specs",
            "DROP TABLE IF EXISTS performance",
            "DROP TABLE IF EXISTS appearance",
            "DROP TABLE IF EXISTS cost",
            "DROP TABLE IF EXISTS car",

            """
            CREATE TABLE car (
                car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                make TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL
            )
            """,

            """
            CREATE TABLE cost (
                car_id INTEGER PRIMARY KEY,
                price REAL,
                location TEXT,
                owner TEXT,
                seller TEXT,
                FOREIGN KEY (car_id) REFERENCES car(car_id)
            )
            """,

            """
            CREATE TABLE appearance (
                car_id  INTEGER PRIMARY KEY,
                color   TEXT,
                length  REAL,
                width   REAL,
                height  REAL,
                seats   INTEGER,
                tank_size REAL,
                FOREIGN KEY (car_id) REFERENCES car(car_id)
            )
            """,

            """
            CREATE TABLE performance (
                car_id INTEGER PRIMARY KEY,
                fuel_type TEXT,
                transmission TEXT,
                kilometers_driven REAL,
                FOREIGN KEY (car_id) REFERENCES car(car_id)
            )
            """,

            """
            CREATE TABLE specs (
                car_id INTEGER PRIMARY KEY,
                drivetrain TEXT,
                engine TEXT,
                max_power TEXT,
                max_torque TEXT,
                FOREIGN KEY (car_id) REFERENCES car(car_id)
            )
            """
        ]
        
        with self.connect() as conn:
            for command in create_tables:
                conn.execute(command)

    # Insertion functions

    def insertCar(self, make, model, year):
        with self.connect() as conn:
            cur = conn.execute("""
                INSERT INTO car (make, model, year)
                VALUES(?, ?, ?)
                """,(make, model, year))

            return cur.lastrowid

    def insertCost(self, cost):
        with self.connect() as conn:
            cur = conn.execute("""
                INSERT INTO cost (car_id, price, location, owner, seller)
                VALUES(?, ?, ?, ?, ?)
                """,(cost.carId, cost.price, cost.loc, cost.own, cost.sellType))
    
    def insertAppearance(self, appear):
        with self.connect() as conn:
            cur = conn.execute("""
                INSERT INTO appearance (car_id, color, length, width, height, seats, tank_size)
                VALUES(?, ?, ?, ?, ?, ?, ?)
                """,(appear.carId, appear.color, appear.length, appear.width, appear.height, appear.seatNum, appear.tank))
    
    def insertPerformance(self, perf):
        with self.connect() as conn:
            cur = conn.execute("""
                INSERT INTO performance (car_id, fuel_type, transmission, kilometers_driven)
                VALUES(?, ?, ?, ?)
                """,(perf.carId, perf.fuel, perf.trans, perf.kilo))
    
    def insertSpecs(self, specs):
        with self.connect() as conn:
            cur = conn.execute("""
                INSERT INTO specs (car_id, drivetrain, engine, max_power, max_torque)
                VALUES(?, ?, ?, ?, ?)
                """,(specs.carId, specs.driveTrain, specs.engine, specs.maxPow, specs.maxTor))

    def importFullCar(self, car, cost, appear, perf, specs):
        # Assumes the connection has been made before this function call and will be closed after
        cur = self.curr
        
        cur.execute("""
            INSERT INTO car (make, model, year)
            VALUES(?, ?, ?)
            """,(car.make, car.model, car.year))

        car_id = cur.lastrowid

        cur.execute("""
            INSERT INTO cost (car_id, price, location, owner, seller)
            VALUES(?, ?, ?, ?, ?)
            """,(car_id, cost.price, cost.loc, cost.own, cost.sellType))

        cur.execute("""
            INSERT INTO appearance (car_id, color, length, width, height, seats, tank_size)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,(car_id, appear.color, appear.length, appear.width, appear.height, appear.seatNum, appear.tank))

        cur.execute("""
            INSERT INTO performance (car_id, fuel_type, transmission, kilometers_driven)
            VALUES(?, ?, ?, ?)
            """,(car_id, perf.fuel, perf.trans, perf.kilo))

        cur.execute("""
            INSERT INTO specs (car_id, drivetrain, engine, max_power, max_torque)
            VALUES(?, ?, ?, ?, ?)
            """,(car_id, specs.driveTrain, specs.engine, specs.maxPow, specs.maxTor))

    # Manual db connection start / stop -> used for optimization during importing car info

    def startDbConn(self):
        self.conn = self.connect()
        self.curr = self.conn.cursor()

    def endDbConn(self):
        self.conn.commit()
        self.curr.close()
        self.conn.close()

    # Filter/view functions

    def isLoaded(self):
        # Used to see if the Database has been loaded with rows (true == rows are filled with something)
        with self.connect() as conn:
            try:
                cur = conn.execute("SELECT COUNT(*) FROM car")
                return cur.fetchone()[0] > 0
            except sqlite3.OperationalError:
                return False

    def getCarDetails(self, carId):
        with self.connect() as conn:
            cur = conn.execute("""
                SELECT cr.car_id, cr.make, cr.model, cr.year, 
                    cst.price, cst.location, cst.owner, cst.seller,
                    app.color, app.length, app.width, app.height, app.seats, app.tank_size,
                    perf.fuel_type, perf.transmission, perf.kilometers_driven,
                    spc.drivetrain, spc.engine, spc.max_power, spc.max_torque
                    FROM car cr
                LEFT JOIN cost cst ON cst.car_id = cr.car_id
                LEFT JOIN appearance app ON app.car_id = cr.car_id
                LEFT JOIN performance perf ON perf.car_id = cr.car_id
                LEFT JOIN specs spc ON spc.car_id = cr.car_id
                WHERE cr.car_id = ?
                """, (carId,))

            result = cur.fetchone()
            if result:
                return list(result)
            else:
                return None

    def executeFilters(self, filters):
        filter_search = """
        SELECT cr.car_id, year, make, model
        FROM car cr
        LEFT JOIN cost cst ON cst.car_id = cr.car_id
        LEFT JOIN appearance app ON app.car_id = cr.car_id
        LEFT JOIN performance perf ON perf.car_id = cr.car_id
        LEFT JOIN specs spc ON spc.car_id = cr.car_id    
        """

        filter_strings = []
        inserted_values = []

        for string, value in filters:
            filter_strings.append(f"{string} = ?")
            inserted_values.append(value)

        filter_search += "WHERE " + " AND ".join(filter_strings)

        with self.connect() as conn:
            cur = conn.execute(filter_search, inserted_values)
            return cur.fetchall()