"""
Created on 19 Feb 2021

@author: conorkiy@gmail.com
"""


import dbinfo
import datetime
import requests
import time
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, insert
import traceback


"""
API variables
"""
NAME="Dublin"
STATIONS="https://api.jcdecaux.com/vls/v1/stations?"


"""
create engine - connect to database
"""
engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/dbikes".format(dbinfo.USER, dbinfo.PASS, dbinfo.URI))

meta = MetaData()
availability = Table(
    'availability', meta,
    Column('number', Integer),
    Column('avail_stands', Integer),
    Column('avail_bikes', Integer),
    Column('status', String(256)),
    Column('last_update', DateTime)
)


"""
main
"""
def main():
    while True:
        try:

            apiRequest = requests.get(STATIONS, params={"contract":NAME, "apiKey": dbinfo.APIKEY})
            values = list(map( get_availability, apiRequest.json() ))
            insert = availability.insert().values(values)
            engine.execute(insert)

            time.sleep(5*60)

        except:

            print(traceback.format_exc())
    
    return


"""
get availability data
"""
def get_availability(stations):
    return {
        'number': stations['number'],
        'avail_stands': stations['available_bike_stands'],
        'avail_bikes': stations['available_bikes'],
        'status': stations['status'],
        'last_update': datetime.datetime.fromtimestamp( stations['last_update'] / 1e3 )
           }
