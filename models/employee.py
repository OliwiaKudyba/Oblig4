from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re

URI = "neo4j+s://c914a714.databases.neo4j.io"
AUTH = ("neo4j", "Z2NG0YLPs6UTaiFNIN5zn1IcY1smIoWpaYgaa8t1IFc")


def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    return driver

def findEmployeeByName(employeename):
    data = _get_connection().execute_query("MATCH (a:Employee) where a.employeename = $employeename RETURN a;", employeename=employeename)
    if len(data[0]) > 0:
        employee = Employee(employeename, data[0][0][0]['email'])
        return employee
    else:
        return Employee(employeename, "Not found in DB")

class Employee:
    def __init__(self, employeename, age, branch):
        self.employeename = employeename
        self.age = age
        self.branch = branch

    def get_EmployeeName(self):
        return self.employeename

    def set_EmployeeName(self, value):
        self.employeename = value

    def get_EmployeeAge(self):
        return self.age

    def set_EmployeeAge(self, value):
        self.age = value

    def get_Branch(self):
        return self.branch

    def set_Branch(self, value):
        self.branch = value