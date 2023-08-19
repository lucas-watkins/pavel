from flask import Flask, request, render_template
from os import system as run_command
from cpanel import cpanel
class Server:

    def getPassword():
        with open('password.txt','r') as f:
            return f.read()
    def parseReferrer(referrer):
        referrer = referrer.replace('http://','')
        print(referrer)
        return referrer[referrer.index('/') + 1:len(referrer)]
    def verifyFromControlPanel(referrer):
        if Server.parseReferrer(referrer) == 'cpanel':
            return True
        else:
            return False
    def run():
        '''Initialize Pavel HTTP server'''
        app = Flask('Pavel'); 
        @app.route("/")
        def main():
            return render_template('main.html')
        
        @app.route("/cpanel", methods = ["POST"])
        def cpanel():
            if request.form.get('password') == Server.getPassword():
                return render_template('controlpanel.html')
            else:
                return "Try again"
        @app.route('/runcommand', methods = ['POST'])
        def runcommand():
            if request.form.get('quickactions') == 'Update Server' and Server.verifyFromControlPanel(request.referrer):
                run_command('sudo apt update && sudo apt upgrade -y')
                return "Server Updated"
            else:
                return "Unknown Action / Invalid Authorization"
        app.run(port = 11251)