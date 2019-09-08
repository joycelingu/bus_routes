import requests
import json
from flask import Flask, jsonify

class Stop:

    lat = ""
    lon = ""
    name = ""

    def __init__(self, dict):
        for key in dict.keys():
            self.name = dict['Name']
            self.lon = dict['Longtitude']
            self.lat = dict['Latitude']

    def getLon(self):
        return self.lon

    def getLat(self):
        return self.lat

    def getName(self):
        return self.name

    def __str__(self):
        returnString = "{" + "Stop: " + str(self.getName()) + ", Longtitude:" + str(self.getLon()) + ", Latitude: " + str(self.getLat()) + "}"
        return returnString

# returns all the stops for a route 'r'.
def all_stops(route_response):
    temporary = route_response.json()
    #print(temporary)
    dict_list = []
    no = ('Key','PointTypeCode','Stop','Rank',"Description",'RouteHeaderRank')
    for item in temporary:
        for keys in no:
            if keys in item.keys():
                del item[keys]
        temp = Stop(item)
        dict_list.append(json.dumps(temp.__dict__))
    return dict_list

def current(b):
    list = b.json()
    d = {}
    for item in list:
        d = item

    delete = ("Static","Driver","APC","RSA")

    for item in delete:
        if item in d:
            del d[item]

    new = {}
    new.update(d['GPS'])
    new.update(d['CurrentWork'])
    Route = new['Route']
    del Route['Key']
    new.update(Route)
    del new['Route']
    del new['Pattern']
    del new['Spd']
    del new['Trip']
    NextStops = d['NextStops']
    d2 = {}
    for i in NextStops:
        d2 = i

    del d2['Key']
    del d2['Work']
    new.update(d2)
    return new

def dataset(n):
    route_numbers = ['01','02','03','04','05','06','07','08','12','15','22','25','26','27','31','34','35','36','40','47',]

    s = requests.get("https://transport.tamu.edu/BusRoutesFeed/api/route/"+route_numbers[n]+"/stops")
    r = requests.get("https://transport.tamu.edu/BusRoutesFeed/api/route/"+route_numbers[n]+"/buses/mentor")
    temp = []
    if len(r.json())>0:
        return all_stops(s), current(r)
    else:
        return (all_stops(s))
    #return str(all_stops(s)),"+"
    #for item in all_stops(s):
        #temp.append(temp)
    #while i<len(all_stops(s)):

    #else:
        #return "false"

#print(dataset(17))

app = Flask(__name__)

def run(i):
    @app.route('/bus_routes')
    def bus_routes():
        return jsonify(dataset(i))
    if __name__ == "__main__":
        app.run(debug=True)

run(17)