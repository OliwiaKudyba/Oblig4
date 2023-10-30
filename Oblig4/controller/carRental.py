from project import app
from flask import render_template, request, redirect, url_for , jsonify
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

'''
@app.route('/order_car', methods=['POST'])
def order_car(customer_id, car_id):
    if customer_id < 0 or customer_id >= len(cars):
        return jsonify({"message" : "Customer not found"}), 404
    if car_id < 0 or car_id >= len(cars):
        return jsonify({"message" : "Car not found"}), 404

    order = order_car(customer_id, car_id)
    return jsonify({"message" : "Car ordered successfully", "order" : order}), 201
'''

@app.route('/order_car', methods=['POST'])
def order_car():
    data = json.loads(request.data)

    customer_name = data.get('name')
    car_reg = data.get('reg')

    if not customer_name or not car_reg:
        return jsonify({'error': 'Both name and registration are required'}), 400

    #Check if customer has a car ordered previously
    existing_orders = find_customer_orders(customer_name)

    if existing_orders:
        return jsonify({'error': 'Customer has already booked a car'}), 400

    #Check and update the status of the car
    car = findCarByReg(car_reg)

    if not car or car.get('status') != 'available':
        return jsonify({'error': 'Car not available for rental, or not found'}), 400

    #update the car status to "booked"
    restult = update_car_status(car_reg, 'booked')

    if restult:
        #create new order
        order_result = create_order(customer_name, car_reg)

        if order_result:
            return jsonify ({'message':'Car has been booked successfully'})
        else:
            return jsonify ({'error': 'Failed to create a new order'}), 500

    else:
        return jsonify ({'error': 'Failed to update car status'}), 500


#Cancel order function
@app.route('/cancel_order_car', methods=['POST'])
def cancel_order_car():
    data = json.loads(request.data)

    customer_name = data.get('name')
    car_reg = data.get('reg')

    if not customer_name or not car_reg:
        return jsonify({'error': 'Both name and registration are needed'}), 400

    #cheks if the car is ordered
    orders = find_orders_by_name_and_reg(customer_name, car_reg)
    if not orders:
        return jsonify({'error': 'Customer has not rented this car'}), 400

    #update the car status to available 
    result = update_car_status(car_reg, 'available')

    if result:
        return jsonify({'message': 'Car booking is now cancelled'})
    else:
        return jsonify({'error': 'Failed to update the status of the car'}), 500

#Rent car function
@app.route('/rent_car', methods=['POST'])
def rent_car():
    data = json.loads(request.data)

    customer_name = data.get('name')
    car_reg = data.get('reg')

    if not customer_name or not car_reg:
        return jsonify({'error': 'Both name and registration are needed'}), 400   

    bookings = find_orders_by_name_and_reg(customer_name, car_reg)

    if not bookings:
        return jsonify({'error': 'Customer does not have a booking for this car'}), 400

    #update the car status to 'rented' 
    result = update_car_status(car_reg, 'rented')

    if result:
        return jsonify({'message': 'Car successfully rented'})
    else:
        return jsonify({'error': 'Failed to update the status of the car to rented'}), 500

#return the car function 
@app.route('/return_car', methods=['POST'])
def return_car():
    data = json.loads(request.data)

    customer_name = data.get('name')
    car_reg = data.get('reg')
    car_status = data_get('status')

    if not customer_name or not car_reg or car_status not in ['ok', 'damaged']:
        return jsonify({'error': 'Name, reg, and valid status are required'}), 400

    bookings = find_orders_by_name_and_reg(customer_name, car_reg)

    if not bookings:
        return jsonify({'error': 'Customer does not have a booking for this car'}), 400

    #Updagte the car status based on the return conditions
    if car_status == 'ok':
        new_status = 'available'
    else:
        new_status = 'damaged'

    result = update_car_status(car_reg, new_status)

    if restult:
        return jsonify({'message': f'Car returned and marked as {new_status}'})
    else:
        return jsonify({'error': 'Failed to update the status of the car to rented'}), 500
