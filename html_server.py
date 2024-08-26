from flask import Flask, render_template,request,make_response,redirect

from p1_meter_reader import P1MeterReader

class HTMLServer:
    def __init__(self,app,api,ip,p1MeterReader):
        self.app = app
        self.api = api
        self.ip = ip
        self.p1MeterReader=p1MeterReader

        @self.app.route("/current-usage")
        def currentUsage():
            serverAddress = ip+":5000"
            print(serverAddress)
            return make_response(render_template('current-usage.html',serverAddress = serverAddress),200)