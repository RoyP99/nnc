'''
Created on 12 jul 2024

@author: robje
'''

from flask import Flask, jsonify, render_template, request, Response
from flask_cors import CORS
#from flask_sock import Sock
from simple_websocket import Server, ConnectionClosed
import html_sse
import json
import requests
import queryws
import threading

# instantiate the app
app = Flask(__name__, static_folder="vue-client/dist/static", template_folder="vue-client/dist", static_url_path="/static")
app.config.from_object(__name__)
#sock = Sock(app)

nmosInfo = {
    'devices': {
    },
    'senders': {
    },
    'receivers': {
    },
}

htmlSse = html_sse.htmlSse()
nmosInfoLock = threading.Lock()
queryWs = queryws.cQueryWs(htmlSse, nmosInfo, nmosInfoLock)

count = 0
parameters = {
    'projects': [ 
        { 'name': 'proj1', 'desc': 'desc1', 'conf': ['conf11', 'conf12'] }, 
        { 'name': 'proj2', 'desc': 'desc1', 'conf': ['conf21', 'conf22'] }, 
        { 'name': 'proj3', 'desc': 'desc1', 'conf': ['conf31', 'conf32'] } 
    ],
    'projectSelected': 'proj2',
    'confSelected': 'conf21' ,
    'settings': { 'registryUrl': '' }
}

settings = { 'registryUrl': '' }

def saveSettings():
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)

def loadSettings():
    global settings
    with open('settings.json') as f:
        settings = json.load(f)
    queryWs.setRegistryUrl(settings['registryUrl'])

def startWebsocket():
    if len(settings['registryUrl']) > 5:
        r = requests.post(settings['registryUrl']+'/subscriptions', json = { 'max_update_rate_ms': 100, 'params' : {}, 'persist': False, 'resource_path': '', 'secure': False })
        js = r.json()
        print(js)
        queryWs.connect(js['ws_href'])

try:
    loadSettings()
    startWebsocket()
except:
    pass

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/", defaults={"path": ""})
#@app.route("/<path:path>")
def index(path):
    return render_template("index.html")

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route("/increment/<int:count>")
def increment(count):
    return f"{count + 1}"

@app.route("/inc")
def inc():
    return jsonify({'count': count + 1})

@app.route("/parameters/<parmNr>", methods=['GET', 'POST'])
def apiParameters(parmNr):
    global parameters
    if request.method == "POST":
        cmd = request.json;
        if parmNr == 'projectSelected':
            parameters['projectSelected'] = cmd['value'] 
            for project in parameters['projects']:
                if project['name'] == parameters['projectSelected']:
                    if len(project['conf']) > 0:
                        parameters['confSelected'] = project['conf'][0]
                    else: 
                        parameters['confSelected'] = ''
        if parmNr == 'confSelected':
            parameters['confSelected'] = cmd['value']
        if parmNr == 'settings':
            settings['registryUrl'] = cmd['registryUrl']
            saveSettings()
            queryWs.setRegistryUrl(settings['registryUrl'])
            startWebsocket()
        if parmNr == 'connectSndRcv':
            # print('connectSndRcv')
            # print(cmd)
            try:
                senderHref = nmosInfo['nodes'][nmosInfo['devices'][nmosInfo['senders'][cmd['senderuuid']]['device_id']]['node_id']]['href'] + 'x-nmos/connection/v1.1/'
                receiverHref = nmosInfo['nodes'][nmosInfo['devices'][nmosInfo['receivers'][cmd['receiveruuid']]['device_id']]['node_id']]['href'] + 'x-nmos/connection/v1.1/'
                # first get transportfile of the sender (SDP)
                url = senderHref + 'single/senders/' + cmd['senderuuid'] + '/transportfile'
                r = requests.get(url)
                # print(r)
                if r.ok:
                    # print(r.content)
                    # now send sdp to receiver
                    req = { 'activation': { 'mode': 'activate_immediate', 'requested_time': None }, 'sender_id': cmd['senderuuid'], 'transport_file': { 'data': r.content.decode('utf-8'), 'type': 'application/sdp'} }
                    url = receiverHref + 'single/receivers/' + cmd['receiveruuid'] + '/staged/'
                    pr = requests.patch(url, json=req)
                    # print('patch send')
                    # print(req)
                    # print(pr)
            except:
                Response(status=404)
        return Response(status=200)
    else:
        if parmNr == 'projects':
            pr = { 'names': [], 'selected': parameters['projectSelected']}
            for project in parameters['projects']:
                pr['names'].append(project['name'])
            return jsonify(pr)
        if parmNr == 'configuration':
            cf = { 'names': [], 'selected': parameters['confSelected']}
            for project in parameters['projects']:
                if project['name'] == parameters['projectSelected']:
                    for conf in project['conf']:
                        cf['names'].append(conf)
                    return jsonify(cf)
        if parmNr == 'description':
            ds = { 'description': '' }
            for project in parameters['projects']:
                if project['name'] == parameters['projectSelected']:
                    ds['description'] = project['desc']
                    return jsonify(ds)
        if parmNr == 'devices':
            #htmlSse.announce(htmlSse.format_sse(json.dumps(nmosInfo['devices']), 'devicesInfo'))
            deviceList = []
            nmosInfoLock.acquire()
            # print(nmosInfo['devices'])
            for fDevice in nmosInfo['devices']:
                dInfo = nmosInfo['devices'][fDevice]
                deviceList.append({'label': dInfo['label'], 'uuid': dInfo['id'], 'description': dInfo['description'], 'type': dInfo['type'] })
            nmosInfoLock.release()
            return jsonify(deviceList)
            #return Response(status=200)
        if parmNr == 'settings':
            return jsonify(settings)
        if parmNr == 'getDeviceReceivers':
            uuid = request.args.get('uuid')
            print(uuid)            
            if uuid in nmosInfo['devices']:
                recvList = []
                rDevice = nmosInfo['devices'][uuid]
                for receiverId in rDevice['receivers']:
                    if receiverId in nmosInfo['receivers']:
                        receiver = nmosInfo['receivers'][receiverId]
                        #recvList.append({'label': receiver['label'], 'uuid': receiver['id'], 'description': receiver['description'], 'format': receiver['format'] })
                        recvList.append(receiver)
            return jsonify(recvList)
        if parmNr == 'getDeviceSenders':
            uuid = request.args.get('uuid')
            print(uuid)            
            if uuid in nmosInfo['devices']:
                senderList = []
                sDevice = nmosInfo['devices'][uuid]
                for senderId in sDevice['senders']:
                    if senderId in nmosInfo['senders']:
                        sender = nmosInfo['senders'][senderId]
                        #senderList.append({'label': sender['label'], 'uuid': sender['id'] })
                        senderList.append(sender)
            return jsonify(senderList)
        return "Record not found", 400

@app.route('/incpost', methods=['POST'])
def incPost():
    global count
    data = request.json
    print(data['myCount'])
    count = data['myCount']
    return data

ws = None

@app.route('/echo', websocket=True)
def echo():
    global ws
    if ws == None:
        ws = Server.accept(request.environ)
    try:
        while True:
            data = ws.receive(1)
            print(data)
            if data != None:
                ws.send(data)
            else:
                pass
                return ''
    except ConnectionClosed:
        print('exception')
        ws = None
    return ''

# add a rule for the URL /listen. This is used by html SSE
app.add_url_rule('/listen', view_func=htmlSse.listenUrl, methods=['GET'])

if __name__ == '__main__':
    app.run()
