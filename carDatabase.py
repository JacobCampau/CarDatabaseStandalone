import psycopg

# MACROS
NAME = "CarInformation"
USER = "postgres"
PASS = "PostgresPass"
HOST = "localhost"
PORT = 5433

class CarDatabase:
    def __init__(self):
        self.databaseInfo = f"dbname = {NAME} user = {USER} password = {PASS} host = {HOST} port = {PORT}"

    def createTables(self):
        createSQL = """
        DROP TABLE IF EXISTS specs;
        DROP TABLE IF EXISTS performance;
        DROP TABLE IF EXISTS appearance;
        DROP TABLE IF EXISTS cost;
        DROP TABLE IF EXISTS car;

        CREATE TABLE car (
            car_id SERIAL PRIMARY KEY,
            make VARCHAR NOT NULL,
            model VARCHAR NOT NULL,
            year INT NOT NULL
        );

        CREATE TABLE cost (
            car_id INT PRIMARY KEY,
            price DOUBLE PRECISION,
            location VARCHAR,
            owner VARCHAR,
            seller VARCHAR,
            FOREIGN KEY (car_id) REFERENCES car(car_id)
        );

        CREATE TABLE appearance (
            car_id INT PRIMARY KEY,
            color VARCHAR,
            length DOUBLE PRECISION,
            width DOUBLE PRECISION,
            height DOUBLE PRECISION,
            seats INT,
            tank_size DOUBLE PRECISION,
            FOREIGN KEY (car_id) REFERENCES car(car_id)
        );

        CREATE TABLE performance (
            car_id INT PRIMARY KEY,
            fuel_type VARCHAR,
            transmission VARCHAR,
            kilometers_driven DOUBLE PRECISION,
            FOREIGN KEY (car_id) REFERENCES car(car_id)
        );

        CREATE TABLE specs (
            car_id INT PRIMARY KEY,
            drivetrain VARCHAR,
            engine VARCHAR,
            max_power VARCHAR,
            max_torque VARCHAR,
            FOREIGN KEY (car_id) REFERENCES car(car_id)
        );
        """
        with psycopg.connect(self.databaseInfo) as conn:
            with conn.cursor() as cur:
                cur.execute(createSQL)

    # Insertion functions

    def insertCar(self, make, model, year):
        with psycopg.connect(self.databaseInfo) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO car (make, model, year)
                VALUES(%s, %s, %s)
                RETURNING car_id
                """,(make, model, year))

                return cur.fetchone()[0]

    def insertCost(self, cost):
        with psycopg.connect(self.databaseInfo) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO cost (car_id, price, location, owner, seller)
                VALUES(%s, %s, %s, %s, %s)
                """,(cost.carId, cost.price, cost.loc, cost.own, cost.sellType))
    
    def insertAppearance(self, appear):
        with psycopg.connect(self.databaseInfo) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO appearance (car_id, color, length, width, height, seats, tank_size)
                VALUES(%s, %s, %s, %s, %s, %s, %s)
                """,(appear.carId, appear.color, appear.length, appear.width, appear.height, appear.seatNum, appear.tank))
    
    def insertPerformance(self, perf):
        with psycopg.connect(self.databaseInfo) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO performance (car_id, fuel_type, transmission, kilometers_driven)
                VALUES(%s, %s, %s, %s)
                """,(perf.carId, perf.fuel, perf.trans, perf.kilo))
    
    def insertSpecs(self, specs):
        with psycopg.connect(self.databaseInfo) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                INSERT INTO specs (car_id, drivetrain, engine, max_power, max_torque)
                VALUES(%s, %s, %s, %s, %s)
                """,(specs.carId, specs.driveTrain, specs.engine, specs.maxPow, specs.maxTor))

    def importFullCar(self, car, cost, appear, perf, specs):
        # Assumes the connection has been made before this function call and will be closed after
        cur = self.curr
        
        cur.execute("""
        INSERT INTO car (make, model, year)
        VALUES(%s, %s, %s)
        RETURNING car_id
        """,(car.make, car.model, car.year))

        carId = cur.fetchone()[0]

        cur.execute("""
        INSERT INTO cost (car_id, price, location, owner, seller)
        VALUES(%s, %s, %s, %s, %s)
        """,(carId, cost.price, cost.loc, cost.own, cost.sellType))

        cur.execute("""
        INSERT INTO appearance (car_id, color, length, width, height, seats, tank_size)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """,(carId, appear.color, appear.length, appear.width, appear.height, appear.seatNum, appear.tank))

        cur.execute("""
        INSERT INTO performance (car_id, fuel_type, transmission, kilometers_driven)
        VALUES(%s, %s, %s, %s)
        """,(carId, perf.fuel, perf.trans, perf.kilo))

        cur.execute("""
        INSERT INTO specs (car_id, drivetrain, engine, max_power, max_torque)
        VALUES(%s, %s, %s, %s, %s)
        """,(carId, specs.driveTrain, specs.engine, specs.maxPow, specs.maxTor))

    # Manual db connection start / stop -> used for optimization during importing car info

    def startDbConn(self):
        self.conn = psycopg.connect(self.databaseInfo)
        self.curr = self.conn.cursor()

    def endDbConn(self):
        self.conn.commit()
        self.curr.close()
        self.conn.close()

    # Filter/view functions

    def getCarDetails(self, carId):
        with psycopg.connect(self.databaseInfo) as conn:
            with conn.cursor() as cur:
                cur.execute("""
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
                WHERE cr.car_id = %s
                """, (carId,))
                result = cur.fetchone()
                if result:
                    return list(result)
                else:
                    return None

    def executeFilters(self, filters):
        filterSearch = """
        SELECT cr.car_id, year, make, model
        FROM car cr
        LEFT JOIN cost cst ON cst.car_id = cr.car_id
        LEFT JOIN appearance app ON app.car_id = cr.car_id
        LEFT JOIN performance perf ON perf.car_id = cr.car_id
        LEFT JOIN specs spc ON spc.car_id = cr.car_id    
        """

        filterStrings = []
        insertedValues = []

        for string, value in filters:
            filterStrings.append(f"{string} = %s")
            insertedValues.append(value)

        filterSearch += "WHERE " + " AND ".join(filterStrings)

        with psycopg.connect(self.databaseInfo) as conn:
            with conn.cursor() as cur:
                cur.execute(filterSearch, insertedValues)
                return cur.fetchall()