from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re
import json

URI = "neo4j+s://c914a714.databases.neo4j.io"
AUTH = ("neo4j", "Z2NG0YLPs6UTaiFNIN5zn1IcY1smIoWpaYgaa8t1IFc")


def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def node_to_json(node): 
    node_properties = dict(node.items()) 
    return node_properties


def findAllCars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in cars] 
        print(nodes_json)
        return nodes_json

def findCarByReg(reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) where a.reg=$reg RETURN a;", reg=reg)    
        print(cars )
        nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)

def save_car(make, model, reg, year, status, location):
    cars = _get_connection().execute_query("MERGE (a:Car{make: $make, model: $model, reg: $reg, year: $year, status:$status, location$location}) RETURN a;", 
        make = make, model = model, reg = reg, year = year, status = status, location = location)
    nodes_json = [node_to_json(record["a"]) for record in cars] 
    print(nodes_json)
    return nodes_json

def update_car(make, model, reg, year, status, location): 
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, a.status = $status, a.location = $location RETURN a;", 
            reg=reg, make=make, model=model, year=year, status = status, location = location)
        print(cars)
        nodes_json = [node_to_json(record["a"]) for record in cars] 
        print(nodes_json)
        return nodes_json

def delete_car(reg):
    _get_connection().execute_query("MATCH (a:Car{reg: $reg}) delete a;", reg = reg)


class Car:
    def __init__(self, carmake, model, year, status, location):
        self.carmake = carmake
        self.model = model
        self.year = year
        self.location = location
        self.status = status 

    def get_Carmake(self):
        return self.carmake

    def set_Carmake(self, value):
        self.carmake = value

    def get_Model(self):
        return self.model

    def set_Model(self, value):
        self.model = value

    def get_year(self):
        return self.year

    def set_year(self, value):
        self.year = value

    def get_CarLoc(self):
        return self.location

    def set_CarLoc(self, value):
        self.location = value

    def get_CarStatus(self):
        return self.status

    def set_CarStatus(self, value):
        self.status = value