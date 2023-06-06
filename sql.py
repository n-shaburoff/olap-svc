# driver sql queries
CREATE_DRIVERS_TABLE = "CREATE TABLE IF NOT EXISTS drivers (id SERIAL PRIMARY KEY, name TEXT);"
INSERT_DRIVER_RETURN_ID = "INSERT INTO drivers (id, name) VALUES (%s, %s) RETURNING id;"
SELECT_ALL_DRIVERS = "SELECT * FROM drivers;"
SELECT_ONE_DRIVER = "SELECT * FROM drivers WHERE id = %s;"
UPDATE_DRIVER_BY_ID = "UPDATE drivers SET name = %s WHERE id = %s;"
DELETE_DRIVER_BY_ID = "DELETE FROM drivers WHERE id = %s;"

# vehicle sql queries
CREATE_VEHICLES_TABLE = "CREATE TABLE IF NOT EXISTS vehicles (id TEXT PRIMARY KEY, brand TEXT, type TEXT, consumption DECIMAL, emission_level DECIMAL, load_capacity DECIMAL);"
INSERT_VEHICLE_RETURN_ID = "INSERT INTO vehicles (id, brand, type, consumption, emission_level, load_capacity) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
SELECT_ALL_VEHICLES = "SELECT * FROM vehicles;"
SELECT_ONE_VEHICLE = "SELECT * FROM vehicles WHERE id = %s;"
UPDATE_VEHICLE_BY_ID = "UPDATE vehicles SET type = %s, brand = %s WHERE id = %s;"
DELETE_VEHICLE_BY_ID = "DELETE FROM vehicles WHERE id = %s;"

# route sql queries 
CREATE_ROUTE_TABLE = 'CREATE TABLE IF NOT EXISTS routes (id SERIAL PRIMARY KEY, distance INTEGER, "from" TEXT, "to" TEXT);'
INSERT_ROUTE_RETURN_ID = 'INSERT INTO routes (id, distance, "from", "to") VALUES (%s, %s, %s, %s) RETURNING id;'
SELECT_ALL_ROUTES = "SELECT * FROM routes;"
SELECT_ONE_ROUTE = "SELECT * FROM routes WHERE id = %s;"
UPDATE_ROUTE_BY_ID = 'UPDATE routes SET distance = %s, "from" = %s, "to" = %s WHERE id = %s;'
DELETE_ROUTE_BY_ID = "DELETE FROM routes WHERE id = %s;"

# transportation sql queries
CREATE_TRANSPORTATION_TABLE = "CREATE TABLE IF NOT EXISTS transportations (id SERIAL PRIMARY KEY, driver_id INTEGER, vehicle_id TEXT, route_id INTEGER, timestamp TIMESTAMP, cargo_weight INTEGER, delivery_cost DECIMAL, emission_per_trip INTEGER, cargo TEXT, FOREIGN KEY (driver_id) REFERENCES drivers (id) ON DELETE SET NULL, FOREIGN KEY (vehicle_id) REFERENCES vehicles (id) ON DELETE SET NULL, FOREIGN KEY (route_id) REFERENCES routes (id) ON DELETE SET NULL);"
INSERT_TRANSPORTATION_RETURN_ID = "INSERT INTO transportations(id, driver_id, vehicle_id, route_id, timestamp, cargo_weight, delivery_cost, emission_per_trip, cargo)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
SELECT_ALL_TRANSPORTATIONS = "SELECT * FROM transportations;"
SELECT_ONE_TRANSPORTATION = "SELECT * FROM transportations WHERE id = %s;"
UPDATE_TRANSPORTATION_BY_ID = "UPDATE transportations SET cargo = %s WHERE id = %s;"
DELETE_TRANSPORTATION_BY_ID = "DELETE FROM transportations WHERE id = %s;"