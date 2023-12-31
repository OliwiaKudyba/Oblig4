from model.cars import _get_connection
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


@app.route('/cancel_order_car', method=['POST'])
def cancel_order_car(customer_id, car_id):
    # Check if the customer has already booked a car
    booked_cars = findCarsBookedByCustomer(Customer.customer_id)
    if booked_cars:
        delete_customer(customer_id)
        delete_car(car_id)
    else: return 0


@app.route('/rent_car', method=['POST'])
def rent_car(customer_id, car_id):
    booked_cars = findCarsBookedByCustomer(Customer.customer_id)
    if booked_cars:
        update_car(car_id.make, car_id.model, car_id.reg, car_id.year, car_id.set_CarStatus(rented), car_id.location)
    else: return 0


@app.route('/return_car', method=['POST'])
def return_car(customer_id, car_id):
    booked_cars = findCarsBookedByCustomer(Customer.customer_id)
    if booked_cars:
        update_car(car_id.make, car_id.model, car_id.reg, car_id.year, car_id.set_CarStatus(available), car_id.location)
    else: return 0



