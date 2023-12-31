from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re
from model.cars import node_to_json


#URI = "neo4j+s://c914a714.databases.neo4j.io"
#AUTH = ("neo4j", "Z2NG0YLPs6UTaiFNIN5zn1IcY1smIoWpaYgaa8t1IFc")
URI = "neo4j+s://7aac58cc.databases.neo4j.io"
AUTH = ("neo4j", "uld_jNEADWDE_ztv27oEFDp_zXEODPtTa8UB62IsJQk")


def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def findAllCustomers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in customers] 
        print(nodes_json)
        return nodes_json

def findCustomerByName(name):
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer) where a.name=$name RETURN a;", name=name)    
        print(customers)
        nodes_json = [node_to_json(record["a"]) for record in customers]
    print(nodes_json)

def create_customer(name, age, address):
    customers = _get_connection().execute_query("MERGE (a:Customer{name: $name, age: $age, address: $address}) RETURN a;", 
        name=name, age=age, address=address)
    nodes_json = [node_to_json(record["a"]) for record in customers] 
    print(nodes_json)
    return nodes_json

def update_customer(name, age, address): 
    with _get_connection().session() as session:
        customers = session.run("MATCH (a:Customer{name:$name}) set a.name=$name, a.age=$age, a.address = $address RETURN a;", 
            name=name, age=age, address=address) 
        print(customers)
        nodes_json = [node_to_json(record["a"]) for record in customers] 
        print(nodes_json)
        return nodes_json

def delete_customer(name):
    _get_connection().execute_query("MATCH (a:Customer{name: $name}) delete a;", name = name)


#small function
def findCarsBookedByCustomer(customer_name):
    query = """
    MATCH (customer:Customer {name: $customer_name})-[:BOOKED]->(car:Car)
    RETURN car
    """
    with _get_connection().session() as session:
        booked_cars = session.run(query, customer_name=customer_name)
        cars_json = [node_to_json(record["car"]) for record in booked_cars]
    return cars_json



class Customer:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def get_CustomerName(self):
        return self.name

    def set_CustomerName(self, value):
        self.name = value

    def get_CustomerAge(self):
        return self.age

    def set_CustomerAge(self, value):
        self.age = value

    def get_CustomerAddress(self):
        return self.address

    def set_CustomerAddress(self, value):
        self.address = value



