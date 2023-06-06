import os 
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, Response, send_file
from sql import *
from datetime import datetime
from flask_cors import CORS
import requests
import matplotlib.pyplot as plt
import matplotlib
from io import BytesIO
import plotly.graph_objects as go
from collections import OrderedDict
import json
from decimal import Decimal

load_dotenv()

app = Flask(__name__)
CORS(app, origins='*')
matplotlib.use('Agg')
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

# drivers routes
@app.route("/api/driver", methods=["POST"])
def create_driver():
    data = request.get_json()
    id = data["id"]
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_DRIVER_RETURN_ID, (id, name,))
            driver_id = cursor.fetchone()[0]
    return {"id": driver_id, "name": name, "message": f"Driver {name} created."}, 201

@app.route("/api/driver", methods=["GET"])
def get_all_drivers():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_DRIVERS)
            drivers = cursor.fetchall()
            if drivers:
                result = []
                for driver in drivers:
                    result.append({"id": driver[0], "name": driver[1]})
                return jsonify(result)
            else:
                return jsonify({"error": f"Drivers not found."}), 404

@app.route("/api/driver/<int:driver_id>", methods=["GET"])
def get_driver(driver_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ONE_DRIVER, (driver_id,)) 
            driver = cursor.fetchone()
            if driver:
                return jsonify({"id": driver[0], "name": driver[1]})
            else:
                return jsonify({"error": f"Driver with ID {driver_id} not found."}), 404
            
@app.route("/api/driver/<int:driver_id>", methods=["PUT"])
def update_driver(driver_id):
    data = request.get_json()
    name = data["name"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_DRIVER_BY_ID, (name, driver_id))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Driver with ID {driver_id} not found."}), 404
    return jsonify({"id": driver_id, "name": name, "message": f"Driver with ID {driver_id} updated."})

@app.route("/api/driver/<int:driver_id>", methods=["DELETE"])
def delete_driver(driver_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_DRIVER_BY_ID, (driver_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Driver with ID {driver_id} not found."}), 404
    return jsonify({"message": f"Driver with ID {driver_id} deleted."})

# vehicles routes
@app.route("/api/vehicle", methods=["POST"])
def create_vehicle():
    data = request.get_json()
    id = data["id"]
    brand = data["brand"]
    type = data["type"]
    consumption = data["consumption"]
    emission_level = data["emission_level"]
    load_capacity = data["load_capacity"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VEHICLE_RETURN_ID, (id, brand, type, consumption, emission_level, load_capacity,))
            vehicle_id = cursor.fetchone()[0]
    return {"id": vehicle_id, "brand": brand, "type": type, "message": f"Vehicle {brand} {type} created."}, 201

@app.route("/api/vehicle", methods=["GET"])
def get_all_vehicles():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_VEHICLES)
            vehicles = cursor.fetchall()
            if vehicles:
                result = []
                for vehicle in vehicles:
                    result.append({"id": vehicle[0], "brand": vehicle[1], "type": vehicle[2]})
                return jsonify(result)
            else:
                return jsonify({"error": f"Vehicles not found."}), 404

@app.route("/api/vehicle/<string:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ONE_VEHICLE, (vehicle_id,)) 
            vehicle = cursor.fetchone()
            if vehicle:
                return jsonify({"id": vehicle[0], "brand": vehicle[1], "type": vehicle[2]})
            else:
                return jsonify({"error": f"Vehicle with ID {vehicle_id} not found."}), 404
            
@app.route("/api/vehicle/<string:vehicle_id>", methods=["PUT"])
def update_vehicle(vehicle_id):
    data = request.get_json()
    type = data["type"]
    brand = data["brand"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_VEHICLE_BY_ID, (type, brand, vehicle_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Vehicle with ID {vehicle_id} not found."}), 404
    return jsonify({"id": vehicle_id, "message": f"Vehicle with ID {vehicle_id} updated."})

@app.route("/api/vehicle/<string:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_VEHICLE_BY_ID, (vehicle_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Vehicle with ID {vehicle_id} not found."}), 404
    return jsonify({"message": f"Vehicle with ID {vehicle_id} deleted."})

# routes routes :D
@app.route("/api/route", methods=["POST"])
def create_route():
    data = request.get_json()
    id = data["id"]
    distance = data["distance"]
    from_city = data["from"]
    to = data["to"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_ROUTE_RETURN_ID, (id, distance, from_city, to,))
            route_id = cursor.fetchone()[0]
    return {"id": route_id, "message": f"Route created."}, 201

@app.route("/api/route", methods=["GET"])
def get_all_routes():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_ROUTES)
            routes = cursor.fetchall()
            if routes:
                result = []
                for route in routes:
                    result.append({"id": route[0], "distance": route[1], "from": route[2], "to": route[3]})
                return jsonify(result)
            else:
                return jsonify({"error": f"Routes not found."}), 404
            
@app.route("/api/route/<int:route_id>", methods=["GET"])
def get_route(route_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ONE_ROUTE, (route_id,)) 
            route = cursor.fetchone()
            if route:
                return jsonify({"id": route[0], "distance": route[1], "from": route[2], "to": route[3]})
            else:
                return jsonify({"error": f"Route with ID {route_id} not found."}), 404
            
@app.route("/api/route/<int:route_id>", methods=["PUT"])
def update_route(route_id):
    data = request.get_json()
    distance = data["distance"]
    from_city = data["from"]
    to = data["to"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_ROUTE_BY_ID, (distance, from_city, to, route_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Route with ID {route_id} not found."}), 404
    return jsonify({"id": route_id, "distance": distance, "from": from_city, "to": to, "message": f"Route with ID {route_id} updated."})

@app.route("/api/route/<int:route_id>", methods=["DELETE"])
def delete_route(route_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_ROUTE_BY_ID, (route_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Route with ID {route_id} not found."}), 404
    return jsonify({"message": f"Route with ID {route_id} deleted."})

# transportations routes 
@app.route("/api/transportation", methods=["POST"])
def create_transportation():
    data = request.get_json()
    id = data["id"]
    driver_id = data["driver_id"]
    vehicle_id = data["vehicle_id"]
    route_id = data["route_id"]
    timestamp = datetime.now()
    cargo_weight = data["cargo_weight"]
    delivery_cost = data["delivery_cost"]
    emission_per_trip = data["emission_per_trip"]
    cargo = data["cargo"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_TRANSPORTATION_RETURN_ID, (id, driver_id,vehicle_id, route_id, timestamp, cargo_weight, delivery_cost, emission_per_trip, cargo))
            transportation_id = cursor.fetchone()[0]
    return {"id": transportation_id, "message": f"Transportation created."}, 201

@app.route("/api/transportation", methods=["GET"])
def get_all_transportations():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_TRANSPORTATIONS)
            transportations = cursor.fetchall()
            if transportations:
                result = []
                for transportation in transportations:
                    result.append(
                        {
                            "id": transportation[0],
                            "driver_id": transportation[1],
                            "vehicle_id": transportation[2],
                            "route_id": transportation[3],
                            "timestamp": transportation[4],
                            "cargo_weight": transportation[5],
                            "delivery_cost": transportation[6],
                            "emission_per_trip": transportation[7],
                            "cargo": transportation[8]
                        })
                return jsonify(result)
            else:
                return jsonify({"error": f"Transportation not found."}), 404
            
@app.route("/api/transportation/<int:transportation_id>", methods=["GET"])
def get_transportation(transportation_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ONE_TRANSPORTATION, (transportation_id,)) 
            transportation = cursor.fetchone()
            if transportation:
                return jsonify({
                            "id": transportation[0],
                            "driver_id": transportation[1],
                            "vehicle_id": transportation[2],
                            "route_id": transportation[3],
                            "timestamp": transportation[4],
                            "cargo_weight": transportation[5],
                            "delivery_cost": transportation[6],
                            "emission_per_trip": transportation[7],
                            "cargo": transportation[8]
                        })
            else:
                return jsonify({"error": f"Transportation with ID {transportation_id} not found."}), 404
            
@app.route("/api/transportation/<int:transportation_id>", methods=["PUT"])
def update_transportation(transportation_id):
    data = request.get_json()
    cargo = data["cargo"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_TRANSPORTATION_BY_ID, (cargo, transportation_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Transportation with ID {transportation_id} not found."}), 404
    return jsonify({"id": transportation_id, "message": f"Transportation with ID {transportation_id} updated."})

@app.route("/api/transportation/<int:transportation_id>", methods=["DELETE"])
def delete_transportation(transportation_id):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_TRANSPORTATION_BY_ID, (transportation_id,))
            if cursor.rowcount == 0:
                return jsonify({"error": f"Transportation with ID {transportation_id} not found."}), 404
    return jsonify({"message": f"Transportation with ID {transportation_id} deleted."})


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

# slice routes 

# Endpoint for Slice 1: Get total delivery cost by driver
@app.route('/slice1')
def get_delivery_cost_by_driver():
    sort_order = request.args.get('sort', default=None)

    with connection:
        with connection.cursor() as cursor:
            query = """
                SELECT name, SUM(delivery_cost)
                FROM transportations
                JOIN drivers ON transportations.driver_id = drivers.id
                GROUP BY name
            """

            if sort_order == 'asc':
                query += " ORDER BY SUM(delivery_cost) ASC"
            elif sort_order == 'desc':
                query += " ORDER BY SUM(delivery_cost) DESC"

            cursor.execute(query)
            result = cursor.fetchall()

            response = OrderedDict()
            for row in result:
                driver_name, total_delivery_cost = row
                response[driver_name] = total_delivery_cost

            json_response = json.dumps(response, cls=DecimalEncoder)

            return Response(json_response, content_type='application/json')
        
# Endpoint for Slice 2: Get total emission per trip by vehicle type
@app.route('/slice2')
def get_emission_per_trip_by_vehicle_type():
    sort_order = request.args.get('sort', default=None)

    with connection:
        with connection.cursor() as cursor:
            query = """
                SELECT type, SUM(emission_per_trip)
                FROM transportations
                JOIN vehicles ON transportations.vehicle_id = vehicles.id
                GROUP BY type
            """

            if sort_order == 'asc':
                query += " ORDER BY SUM(emission_per_trip) ASC"
            elif sort_order == 'desc':
                query += " ORDER BY SUM(emission_per_trip) DESC"

            cursor.execute(query)
            result = cursor.fetchall()

            response = OrderedDict()
            for row in result:
                vehicle_type, total_emission = row
                response[vehicle_type] = total_emission

        json_response = json.dumps(response, cls=DecimalEncoder)

        return Response(json_response, content_type='application/json')
        
# Endpoint for Slice 3: Get average cargo weight by route
@app.route('/slice3')
def get_average_cargo_weight_by_route():
    sort_order = request.args.get('sort', default=None)
    
    with connection:
        with connection.cursor() as cursor:
            query = """
                SELECT "from", "to", AVG(cargo_weight)
                FROM transportations
                JOIN routes ON transportations.route_id = routes.id
                GROUP BY routes.id
            """

            if sort_order == 'asc':
                query += " ORDER BY AVG(cargo_weight) ASC"
            elif sort_order == 'desc':
                query += " ORDER BY AVG(cargo_weight) DESC"

            cursor.execute(query)
            result = cursor.fetchall()

            response = OrderedDict()
            for row in result:
                fromCity,to, average_cargo_weight = row
                response[fromCity+ " - " +to] = average_cargo_weight

        json_response = json.dumps(response, cls=DecimalEncoder)

        return Response(json_response, content_type='application/json')

# Endpoint Slice 4: Get the average delivery cost per driver  
@app.route('/slice4')
def get_average_delivery_cost_by_driver():
    sort_order = request.args.get('sort', default=None)

    with connection:
        with connection.cursor() as cursor:
            query = """
                SELECT name, AVG(delivery_cost) as average_delivery_cost
                FROM transportations
                JOIN drivers ON transportations.driver_id = drivers.id
                GROUP BY name
            """

            if sort_order == 'asc':
                query += " ORDER BY AVG(delivery_cost) ASC"
            elif sort_order == 'desc':
                query += " ORDER BY AVG(delivery_cost) DESC"

            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()

            response = OrderedDict()
            for row in result:
                driver_name, average_delivery_cost = row
                response[driver_name] = average_delivery_cost

        json_response = json.dumps(response, cls=DecimalEncoder)

        return Response(json_response, content_type='application/json')

# Endpoint for Slice 5: Get total delivery cost by cargo type
@app.route('/slice5')
def get_delivery_cost_by_cargo_type():
    sort_order = request.args.get('sort', default=None)

    with connection:
        with connection.cursor() as cursor:
            query = """
                SELECT cargo, SUM(delivery_cost)
                FROM transportations
                GROUP BY cargo
            """

            if sort_order == 'asc':
                query += " ORDER BY SUM(delivery_cost) ASC"
            elif sort_order == 'desc':
                query += " ORDER BY SUM(delivery_cost) DESC"

            cursor.execute(query)
            result = cursor.fetchall()

            response = OrderedDict()
            for row in result:
                cargo_type, total_delivery_cost = row
                response[cargo_type] = total_delivery_cost

        json_response = json.dumps(response, cls=DecimalEncoder)

        return Response(json_response, content_type='application/json')
        
@app.route('/chart1')
def generate_chart1():
    import matplotlib
    matplotlib.use('Agg')

    # Fetch data from Slice 1
    response = requests.get('http://localhost:5000/slice1')
    data = response.json()

    # Extract driver names and total delivery costs
    driver_names = list(data.keys())
    delivery_costs = list(data.values())

    # Convert delivery costs to float values
    delivery_costs = [float(cost) for cost in delivery_costs]

    # Create the chart
    plt.figure(figsize=(10, 6))
    plt.subplots_adjust(bottom=0.3)
    plt.bar(driver_names, delivery_costs, color='lightblue')
    plt.xlabel('Driver', fontsize=12)
    plt.ylabel('Total Delivery Cost', fontsize=12)
    plt.title('Total Delivery Cost by Driver', fontsize=14)

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45, ha='right')

    # Add the value labels to the bars
    for i, cost in enumerate(delivery_costs):
        plt.text(i, cost, str(cost), ha='center', va='bottom')

    # Convert the chart to an image and return it
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    return send_file(image_stream, mimetype='image/png')

@app.route('/chart2')
def generate_chart2():
    import matplotlib
    matplotlib.use('Agg')

    # Fetch data from Slice 2
    response = requests.get('http://localhost:5000/slice2')
    data = response.json()

    # Extract vehicle types and emission per trip values
    vehicle_types = list(data.keys())
    emissions = list(data.values())

    # Create the chart
    plt.figure(figsize=(10, 6))
    plt.subplots_adjust(bottom=0.3)
    plt.plot(vehicle_types, emissions, marker='o', color='lightgreen', linestyle='-', linewidth=2)
    plt.xlabel('Vehicle Type', fontsize=12)
    plt.ylabel('Emission per Trip', fontsize=12)
    plt.title('Emission per Trip by Vehicle Type', fontsize=14)

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45, ha='right')

    # Convert the chart to an image and return it
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    return send_file(image_stream, mimetype='image/png')

@app.route('/chart3')
def generate_chart3():
    import matplotlib
    matplotlib.use('Agg')

    # Fetch data from Slice 3
    response = requests.get('http://localhost:5000/slice3')
    data = response.json()

    # Extract route names and average cargo weights
    route_names = list(data.keys())
    average_weights = list(data.values())

    # Convert average cargo weights to float values
    average_weights = [float(weight) for weight in average_weights]

    # Create the chart
    plt.figure(figsize=(10, 6))
    plt.subplots_adjust(bottom=0.3)  # Adjust the bottom spacing for the x-axis labels

    # Plot the bar chart
    plt.bar(route_names, average_weights, color='orange')

    plt.xlabel('Route', fontsize=12)
    plt.ylabel('Average Cargo Weight', fontsize=12)
    plt.title('Average Cargo Weight by Route', fontsize=14)

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45, ha='right')

    # Add the value labels to the bars
    for i, weight in enumerate(average_weights):
        plt.text(i, weight, str(weight), ha='center', va='bottom')

    # Convert the chart to an image and return it
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png', bbox_inches='tight')  # Adjust the bounding box
    plt.close()
    image_stream.seek(0)

    return send_file(image_stream, mimetype='image/png')

@app.route('/chart4')
def generate_chart4():
    import matplotlib
    matplotlib.use('Agg')

    # Fetch data from Slice 4
    response = requests.get('http://localhost:5000/slice4')
    data = response.json()

    # Extract vehicle brands and delivery costs
    brands = list(data.keys())
    delivery_costs = list(data.values())

    # Convert delivery costs to float values
    delivery_costs = [float(cost) for cost in delivery_costs]

    # Create the chart
    plt.figure(figsize=(10, 6))
    plt.subplots_adjust(bottom=0.3)
    plt.bar(brands, delivery_costs, color='skyblue')
    plt.xlabel('Vehicle Brand', fontsize=12)
    plt.ylabel('Delivery Cost', fontsize=12)
    plt.title('Top Vehicle Brands by Delivery Cost', fontsize=14)

    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45, ha='right')

    # Add the value labels to the bars
    for i, cost in enumerate(delivery_costs):
        plt.text(i, cost, str(cost), ha='center', va='bottom')

    # Convert the chart to an image and return it
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    return send_file(image_stream, mimetype='image/png')

@app.route('/chart5')
def generate_chart5():
    import matplotlib
    matplotlib.use('Agg')

    response = requests.get('http://localhost:5000/slice5')
    data = response.json()

    cargo_types = list(data.keys())
    delivery_costs = list(data.values())

    delivery_costs = [float(cost) for cost in delivery_costs]

    plt.figure(figsize=(10, 6))
    plt.subplots_adjust(bottom=0.3)
    plt.bar(cargo_types, delivery_costs, color='gold')
    plt.xlabel('Cargo Type', fontsize=12)
    plt.ylabel('Delivery Cost', fontsize=12)
    plt.title('Delivery Cost by Cargo Type', fontsize=14)

    plt.xticks(rotation=45, ha='right')

    for i, cost in enumerate(delivery_costs):
        plt.text(i, cost, str(cost), ha='center', va='bottom')

    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()
    image_stream.seek(0)

    return send_file(image_stream, mimetype='image/png')

@app.route('/dynamic_chart1')
def dynamic_chart1():
    response = requests.get('http://localhost:5000/slice1')  
    data = response.json()

    drivers = []
    delivery_costs = []
    for driver, cost in data.items():
        drivers.append(driver)
        delivery_costs.append(cost)

    fig = go.Figure(data=[go.Pie(labels=drivers, values=delivery_costs, hole=0.4)])
    fig.update_layout(
    title={
        'text': "Total delivery cosr by driver",
        'x': 0.5,  
        'y': 0.9,  
        'xanchor': 'center',  
        'yanchor': 'top',  
        'font': {'size': 24}  
    }
)

    chart_data = fig.to_json()

    return chart_data

@app.route('/dynamic_chart2')
def dynamic_chart2():
    response = requests.get('http://localhost:5000/slice2') 
    data = response.json()

    vehicle_types = []
    emission_per_trip = []
    for vehicle_type, emission in data.items():
        vehicle_types.append(vehicle_type)
        emission_per_trip.append(emission)

    fig = go.Figure(data=[go.Bar(x=vehicle_types, y=emission_per_trip)])
    fig.update_layout(
    title={
        'text': "Emission per Trip by Vehicle Type",
        'x': 0.5,  
        'y': 0.9,  
        'xanchor': 'center',  
        'yanchor': 'top',  
        'font': {'size': 24}  
    })

    chart_data = fig.to_json()

    return chart_data

@app.route('/dynamic_chart3')
def dynamic_chart3():
    response = requests.get('http://localhost:5000/slice3')  
    data = response.json()

    routes = []
    average_cargo_weight = []
    for route, cargo_weight in data.items():
        routes.append(route)
        average_cargo_weight.append(float(cargo_weight))  

    fig = go.Figure(data=[go.Bar(x=routes, y=average_cargo_weight)])
    fig.update_layout(
    title={
        'text': "Average Cargo Weight by Route",
        'x': 0.5,  
        'y': 0.9,  
        'xanchor': 'center',  
        'yanchor': 'top', 
        'font': {'size': 24}  
    })

    chart_data = fig.to_json()

    return chart_data
     
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()