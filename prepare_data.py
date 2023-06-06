import psycopg2
from sql import *

connection = psycopg2.connect("postgres://postgres:trewQ1234@localhost/postgres?sslmode=disable")

cur = connection.cursor()

def import_data(createQuery, fileName, tableName):
    cur.execute(createQuery)
    connection.commit()
  
    with open(fileName, 'r') as f:
        next(f) 
        cur.copy_from(f, tableName, sep=',')

    connection.commit()

# importings
import_data(CREATE_DRIVERS_TABLE, 'data/drivers.csv', 'drivers')
print("drivers - success")

import_data(CREATE_VEHICLES_TABLE, 'data/vehicles.csv', 'vehicles')
print("vehicles - success")

import_data(CREATE_ROUTE_TABLE, 'data/routes.csv', 'routes')
print("routes - success")

import_data(CREATE_TRANSPORTATION_TABLE, 'data/transportations.csv', 'transportations')
print("transportations - success")