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

def findAllEmployees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in employees] 
        print(nodes_json)
        return nodes_json

def findEmployeeByName(name):
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee) where a.name=$name RETURN a;", name=name)    
        print(employees)
        nodes_json = [node_to_json(record["a"]) for record in employees]
    print(nodes_json)

def create_employee(name, address, branch):
    employees = _get_connection().execute_query("MERGE (a:Employee{name: $name, address: $address, branch: $branch}) RETURN a;", 
        name=name, address=address, branch=branch)
    nodes_json = [node_to_json(record["a"]) for record in employees] 
    print(nodes_json)
    return nodes_json

def update_employee(name, address, branch): 
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee{name:$name}) set a.name=$name, a.address=$address, a.branch = $branch RETURN a;", 
            name=name, address=address, branch=branch) 
        print(employees)
        nodes_json = [node_to_json(record["a"]) for record in employees] 
        print(nodes_json)
        return nodes_json

def delete_employee(name):
    _get_connection().execute_query("MATCH (a:Employee{name: $name}) delete a;", name = name)

class Employee:
    def __init__(self, name, address, branch):
        self.name = name
        self.address = address
        self.branch = branch

    def get_EmployeeName(self):
        return self.name

    def set_EmployeeName(self, value):
        self.name = value

    def get_EmployeeAddress(self):
        return self.address

    def set_EmployeeAddress(self, value):
        self.adress = value

    def get_Branch(self):
        return self.branch

    def set_Branch(self, value):
        self.branch = value