from cloudmesh.common.FlatDict import FlatDict
from cloudmesh.common.Printer import Printer
import pytest

data = {
    "name":"Daivik",
    "address": {
        "city":"Bloomington",
        "state":"Indiana",
        "country":"United States"

                }
        }

flat = FlatDict(data,sep='__')

def table_test(self):
    table = Printer.flatwrite(self.data,sort_keys=["name"],order=["name","address.city","address.state"],header=["Name","City","State"],output='table')
    print(table)

