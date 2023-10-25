from project import app
from flask import render_template, request, redirect, url_for 
from model.cars import *
from model.customer import *
from model.employee import *

###CARS
@app.route('/create_car', methods=["POST"]) 
def create_car_info():    
    record = json.loads(request.data)
    print(record)
    return save_car(record['make'], record['model'], record['reg'], record['year'], record['status'], record['location'] )

@app.route('/update_car', methods=['PUT'])
def update_car_info():
    record = json.loads(request.data)
    print(record)
    return update_car(record['make'], record['model'], record['reg'], record['year'], record['status'], record['location'])

@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = json.loads(request.data) 
    print(record) 
    delete_car(record['reg'])
    return findAllCars()

@app.route('/read_car', method=['GET'])
def read_car_info():
    record = json.loads(request.data)
    print(record)
    return findCarByReg(record['reg'])

####CUSTOMER
@app.route('/create_customer', methods=["POST"]) 
def create_customer_info():    
    record = json.loads(request.data)
    print(record)
    return create_customer(record['name'], record['age'], record['address'])

@app.route('/update_customer', methods=['PUT'])
def update_customer_info():
    record = json.loads(request.data)
    print(record)
    return update_customer(record['name'], record['age'], record['address'])

@app.route('/delete_customer', methods=['DELETE'])
def delete_customer_info():
    record = json.loads(request.data) 
    print(record) 
    delete_customer(record['name'])
    return findAllCustomers()

@app.route('/read_customer', method=['GET'])
def read_customer_info():
    record = json.loads(request.data)
    print(record)
    return findCustomerByName(record['name'])


###EMPLOYEE
@app.route('/create_employee', methods=["POST"]) 
def create_employee_info():    
    record = json.loads(request.data)
    print(record)
    return create_employee(record['name'], record['address'], record['branch'])

@app.route('/update_employee', methods=['PUT'])
def update_employee_info():
    record = json.loads(request.data)
    print(record)
    return update_employee(record['name'], record['address'], record['branch'])

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    record = json.loads(request.data) 
    print(record) 
    delete_employee(record['name'])
    return findAllEmployees()

@app.route('/read_employee', method=['GET'])
def read_employee_info():
    record = json.loads(request.data)
    print(record)
    return findEmployeeByName(record['name'])

@app.route('/order_car', methods=['POST'])
def order_car(customer_id, car_id):
    if customer_id < 0 or customer_id >= len(cars):
        return jsonify({"message" : "Customer not found"}), 404
    if car_id < 0 or car_id >= len(cars):
        return jsonify({"message" : "Car not found"}), 404

    order = order_car(customer_id, car_id)
    return jsonify({"message" : "Car ordered successfully", "order" : order}), 201
