from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re

URI = "neo4j+s://c914a714.databases.neo4j.io"
AUTH = ("neo4j", "Z2NG0YLPs6UTaiFNIN5zn1IcY1smIoWpaYgaa8t1IFc")


def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    return driver

def findCustomerByName(customername):
    data = _get_connection().execute_query("MATCH (a:Customer) where a.customername = $customername RETURN a;", customername=customername)
    if len(data[0]) > 0:
        customer = Customer(customername, data[0][0][0]['email'])
        return customer
    else:
        return Customer(customername, "Not found in DB")

class Customer:
    def __init__(self, customername, age, address):
        self.customername = customername
        self.age = age
        self.address = address

    def get_CustomerName(self):
        return self.customername

    def set_CustomerName(self, value):
        self.customername = value

    def get_CustomerAge(self):
        return self.age

    def set_CustomerAge(self, value):
        self.age = value

    def get_CustomerAddress(self):
        return self.address

    def set_CustomerAddress(self, value):
        self.address = value



CREATE (charlie:Person:Costumer {name: 'Charlie Sheen', age: "38", adress: "TullogTøysveien 3"}),


CREATE (charlie:Person:Costumer {name: 'Charlie Sheen', age: "38", adress: "TullogTøysveien 3"}),
(sarah:Person:Employee {name: 'Sarah Tomson', age: "30", adress: "TullogTøysveien 10"}), 
(car:Car:Car {type: 'Nissan', reg: "EL9999", model: "1995"})