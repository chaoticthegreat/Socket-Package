from sock import server
server.listen("0.0.0.0",8080)
input()
server.send("hi","server")
print(server.clientmessages)