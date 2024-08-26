import json
import datetime
import calendar

from flask import Flask
from flask import request
from flask_restful import Resource, Api

from p1_meter_reader import P1MeterReader
from models import MeterReading, MeterReadings
from types import SimpleNamespace



#server
class RestServer:
    def __init__(self,app,api, p1MeterReader):
        self.app = app
        self.api = api
        self.p1MeterReader = p1MeterReader
                
        print("Started Rest Server")

        @self.app.route('/api/current', methods=['GET'])  
        def getCurrent():
            parsed = toJson(self.p1MeterReader.lastReading)
            print(parsed)
            return parsed, 200
        
        @self.app.route('/api/history', methods=['GET'])  
        def getHistory():
            args = request.args.to_dict()
            print("history arguments: "+str(args))
            
            res = int(args["res"])
            print("type?: "+str(type(self.p1MeterReader.meterReadings.readings)))
            
            cutoffSeconds = calendar.timegm(datetime.datetime.now().timetuple())-res
            filtered = []
            for mr in self.p1MeterReader.meterReadings.readings:
                if(mr.timestamp >= cutoffSeconds):
                    filtered.append(mr)
                
            
            
            parsed = MeterReadings(filtered).toJson()
            print(parsed)
            return parsed, 200
        
        @self.app.route('/api/store-history', methods=['GET'])  
        def storeHistory():
            
            data = p1MeterReader.meterReadings.toJson()

            f = open("../history-data.json", "w")
            f.write(data)
            f.close()
            
            stored = len(data)
            return '{"count":'+str(stored)+'}', 200
        
        @self.app.route('/api/load-history', methods=['GET'])  
        def loadHistory():
            
            f = open("../history-data.json", "r")
            jsonData = f.read()
            parsedData = json.loads(jsonData, object_hook=lambda d: SimpleNamespace(**d))
            print("loaded "+str(parsedData))

            mrs = []
            for r in parsedData.readings:
                mr = MeterReading(r.date,r.timestamp,r.usageWatts)
                mrs.append(mr)
                
            m = MeterReadings(mrs)
            p1MeterReader.meterReadings = m
            
            
            read = len(mrs)
            return '{"Loaded":'+str(read)+'}', 200


def toJson(obj):
    return json.dumps(obj.__dict__)
