from flask import Flask, request
import requests, threading

host = None
port = None
app = Flask(__name__)
clientmessages = {}
clienttrack = {}

def listen(hoster, porter):
  global clientmessages
  clientmessages["server"] = []
  global host, port
  host = hoster
  port = porter
  def run():
    app.run(hoster, porter)
  threading.Thread(target = run).start()
@app.route("/send", methods = ["POST"])
def sender():
  global clientmessages
  json = request.json
  clientmessages[json["client"]].append(json["message"])
  return "sent"
@app.route("/connect", methods = ["POST"])
def connect():
  global clientmessages, clienttrack
  json = request.json
  clientmessages[json["client"]] = []
  clienttrack[json["client"]] = None
@app.route("/recv", methods = ["GET"])
def recieve():
  global clienttrack
  json = request.json
  if len(clientmessages[json["client"]]) == clienttrack[json["client"]]:
    return "nothing"
  else:
    clienttrack[json["client"]] = len(clientmessages[json["client"]])
    return clientmessages[json["client"]][len(clientmessages[json["client"]])]
def send(message, client):
  requests.post("https://"+host+"/send", json = {"client":client, "message":message})