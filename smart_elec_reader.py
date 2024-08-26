import socket
import threading

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from config_manager import ConfigManager
from p1_meter_reader import P1MeterReader
from rest_server import RestServer
from html_server import HTMLServer
from error_server import ErrorServer


#method to get the ip address in the network that the pi is running on
def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '0.0.0.0'
    finally:
        s.close()
    return IP

ip = getIp()
print("Pi is running on IP: "+ip)

#config
config = ConfigManager()
config.load()

#meter reader
p1MeterReader = P1MeterReader()

p1ReaderThread = threading.Thread(target = p1MeterReader.runReader, args = ())
p1ReaderThread.start()

#servers
app = Flask(__name__,static_url_path='',static_folder='web/static',template_folder='web/templates')

CORS(app)

api = Api(app)

errorServer = ErrorServer(app,api)
restServer = RestServer(app,api,p1MeterReader)
if config.httpServerEnabled == True:
    htmlServer = HTMLServer(app,api,ip,p1MeterReader)


app.run(debug=False,host="0.0.0.0",threaded=True)




    
