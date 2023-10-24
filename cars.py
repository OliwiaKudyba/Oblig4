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

def findCarByMake(carmake):
    data = _get_connection().execute_query("MATCH (a:Car) where a.carmake = $carmake RETURN a;", carmake=carmake)
    if len(data[0]) > 0:
        car = Car(carmake, data[0][0][0]['email'])
        return car
    else:
        return Car(carmake, "Not found in DB")

class Car:
    def __init__(self, carmake, model, year, location, status):
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