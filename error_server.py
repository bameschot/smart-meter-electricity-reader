from flask import Flask, render_template,request,make_response,redirect

class ErrorServer:
    def __init__(self,app,api):
        self.app = app
        self.api = api

        
        @self.app.errorhandler(Exception)
        def notfound(error):
            return {
                "code":error.code,
                "name":error.name
                },error.code

        