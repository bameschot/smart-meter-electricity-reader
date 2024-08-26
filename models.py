import json

class MeterReadings:
    def __init__(self, readings):
        self.readings = readings
    
    def toJson(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)

class MeterReading:
    def __init__(
            self,
            date,
            timestamp,
            usageWatts):
        self.date = date
        self.timestamp=timestamp
        self.usageWatts = usageWatts
    
    def toJson(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4)