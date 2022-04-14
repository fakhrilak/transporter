import socketio
import requests
import json
import time
sio = socketio.Client()
sio.connect('https://trymulti.zilog.club',namespaces=['/'])

@sio.on("res-onConnect")
def on_connect(data):
    print(data)

@sio.on("sametokengenerate")
def on_connect(data):
    try:
        res = ""
        print(data)
        if data["method"] == "GET":
            if data["auth"] == False:
                res = requests.get(data["endpoint"]+data["params"])
            elif data["auth"] == True:
                print("masuk sini",data)
                res = requests.get(data["endpoint"],headers=data["headers"])
                print(res.text)
        elif data["method"] == "POST":
            if data["auth"] == True:
                res = requests.post(data["endpoint"], data = data["body"],headers=data["headers"] )
            elif data["auth"] == False:
                res = requests.post(data["endpoint"], data = data["body"] )
        elif data["method"] == "PATCH":
            if data["auth"] == True:
                res = requests.patch(data["endpoint"], data = data["body"],headers=data["headers"] )
        print(res.status_code)
        newdata = {
            "socketID":data["socketID"],
            "response":json.dumps({
              "status":int(res.status_code),
              "data" : res.text,
	      "path" : data["path"]
            })
        }
        # newdata = json.loads(newdata)
        sio.emit("onRes-Data",newdata)
    except BaseException as err:
        newdata = {
            "socketID":data["socketID"],
            "response":str(err)
        }
        sio.emit("onRes-Data",newdata)
sio.emit("onConnect",{"message":"Connected"})
sio.wait()
